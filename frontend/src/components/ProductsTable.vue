<template>
  <div class="products-table">
    <!-- Диаграммы -->
    <el-row :gutter="20" class="charts">
      <el-col :span="12">
        <canvas ref="priceHistogramCanvas" id="priceHistogram"></canvas>
      </el-col>
      <el-col :span="12">
        <canvas ref="discountVsRatingCanvas" id="discountVsRating"></canvas>
      </el-col>
    </el-row>

    <!-- Фильтры -->
    <el-row :gutter="20" class="filters">
      <!-- Слайдер для диапазона цен -->
      <el-col :span="8">
        <el-form-item label="Диапазон цен">
          <el-slider
            v-model="priceRange"
            range
            :min="minPrice"
            :max="maxPrice"
            :step="1"
            @change="applyFilters"
          />
        </el-form-item>
      </el-col>
      <!-- Фильтр по минимальному рейтингу -->
      <el-col :span="8">
        <el-form-item label="Мин. рейтинг">
          <el-input-number
            v-model="minRating"
            :min="0"
            :max="5"
            :step="0.1"
            @change="applyFilters"
          />
        </el-form-item>
      </el-col>
      <!-- Фильтр по минимальному кол-ву отзывов -->
      <el-col :span="8">
        <el-form-item label="Мин. отзывы">
          <el-input-number
            v-model="minReviews"
            :min="0"
            :step="10"
            @change="applyFilters"
          />
        </el-form-item>
      </el-col>
    </el-row>

    <!-- Таблица товаров -->
    <el-table
      :data="products"
      style="width: 100%"
      @sort-change="handleSortChange"
    >
      <el-table-column prop="name" label="Название" sortable />
      <el-table-column prop="price" label="Цена" sortable width="120">
        <template #default="{ row }">
          {{ row.price.toFixed(2) }} ₽
        </template>
      </el-table-column>
      <el-table-column prop="discounted_price" label="Цена со скидкой" sortable width="180">
        <template #default="{ row }">
          {{ row.discounted_price.toFixed(2) }} ₽
        </template>
      </el-table-column>
      <el-table-column prop="rating" label="Рейтинг" sortable width="120" />
      <el-table-column prop="review_count" label="Отзывы" sortable width="120" />
    </el-table>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import axios from 'axios'

// Данные для таблицы и фильтров
const products = ref([])
const priceRange = ref([0, 0]) // диапазон цен
const minPrice = ref(0) // Динамическая минимальная цена
const maxPrice = ref(0) // Динамическая максимальная цена
const minRating = ref(null) // Минимальный рейтинг
const minReviews = ref(null) // Минимальное количество отзывов
const sortField = ref(null) // Поле для сортировки
const sortOrder = ref(null) // Направление сортировки (asc/desc)

// Ссылки и объекты для диаграмм
const priceHistogramCanvas = ref(null)
const discountVsRatingCanvas = ref(null)
let priceHistogram = null
let discountVsRatingChart = null

// Установка начального диапазона цен
const setInitialPriceRange = async () => {
  try {
    const response = await axios.get('http://localhost:8000/api/products/')
    products.value = response.data
    const allProducts = response.data
    if (allProducts.length > 0) {
      const prices = allProducts.map(product => product.price)
      minPrice.value = Math.min(...prices)
      maxPrice.value = Math.max(...prices)
      priceRange.value = [minPrice.value, maxPrice.value]
      updateCharts()
    } else {
      minPrice.value = 0
      maxPrice.value = 0
      priceRange.value = [0, 0]
    }
  } catch (error) {
    console.error('Ошибка при загрузке начального диапазона:', error)
    minPrice.value = 0
    maxPrice.value = 0
    priceRange.value = [0, 0]
  }
}

// Установка priceRange в пределах minPrice и maxPrice
const constrainPriceRange = () => {
  priceRange.value[0] = Math.max(minPrice.value, priceRange.value[0])
  priceRange.value[1] = Math.min(maxPrice.value, priceRange.value[1])
}

// Обновление диаграмм
const updateCharts = () => {
  if (priceHistogram) priceHistogram.destroy()
  if (discountVsRatingChart) discountVsRatingChart.destroy()

  // Гистограмма цен
  const priceData = {}
  if (products.value.length > 0) {
    const currentMin = priceRange.value[0]
    const currentMax = priceRange.value[1]
    const priceStep = (currentMax - currentMin) / 10
    if (priceStep > 0) {
      products.value.forEach(product => {
        const bin = Math.floor((product.price - currentMin) / priceStep) * priceStep + currentMin
        if (bin >= currentMin && bin <= currentMax) {
          priceData[bin] = (priceData[bin] || 0) + 1
        }
      })
      const priceLabels = Object.keys(priceData).map(Number).sort((a, b) => a - b)
      const priceCounts = priceLabels.map(label => priceData[label])
      const labelFormat = (label) => `${Math.round(label)}-${Math.round(label + priceStep)}`

      priceHistogram = new Chart(priceHistogramCanvas.value, {
        type: 'bar',
        data: {
          labels: priceLabels.map(labelFormat),
          datasets: [{
            label: 'Количество товаров',
            data: priceCounts,
            backgroundColor: 'rgba(75, 192, 192, 0.2)',
            borderColor: 'rgba(75, 192, 192, 1)',
            borderWidth: 1
          }]
        },
        options: {
          scales: {
            y: { beginAtZero: true, title: { display: true, text: 'Количество' } },
            x: { title: { display: true, text: 'Диапазон цен (руб)' } }
          }
        }
      })
    }
  }

  // Линейный график средний размер скидок на товар vs рейтинг товара
  const discountData = products.value.map(product => ({
    discount: product.price - product.discounted_price,
    rating: product.rating || 0
  }))

  const ratings = Array.from({ length: 51 }, (_, i) => i * 0.1) // Шаг 0.1 от 0 до 5
  const averagedData = ratings.map(rating => {
    const filtered = discountData.filter(d => Math.abs(d.rating - rating) < 0.05)
    return filtered.length ? filtered.reduce((sum, d) => sum + d.discount, 0) / filtered.length : null
  })

  discountVsRatingChart = new Chart(discountVsRatingCanvas.value, {
    type: 'line',
    data: {
      labels: ratings.map(r => r.toFixed(1)),
      datasets: [{
        label: 'Средний размер скидки (руб)',
        data: averagedData,
        fill: false,
        borderColor: 'rgb(255, 99, 132)',
        tension: 0.1,
        spanGaps: true
      }]
    },
    options: {
      scales: {
        y: { beginAtZero: true, title: { display: true, text: 'Размер скидки' } },
        x: {
          title: { display: true, text: 'Рейтинг' },
          ticks: { stepSize: 0.1, min: 0, max: 5 },
          type: 'linear'
        }
      }
    }
  })
}

// Загрузка товаров с учетом фильтров
const fetchProducts = async () => {
  try {
    const params = {
      min_price: priceRange.value[0],
      max_price: priceRange.value[1],
      min_rating: minRating.value,
      min_reviews: minReviews.value,
      ordering: sortField.value ? (sortOrder.value === 'descending' ? `-${sortField.value}` : sortField.value) : null,
    }

    Object.keys(params).forEach((key) => params[key] == null && delete params[key])

    const response = await axios.get('http://localhost:8000/api/products/', { params })
    products.value = response.data
    updateCharts()
  } catch (error) {
    console.error('Ошибка при загрузке товаров:', error)
  }
}

// Обработчик изменения сортировки
const handleSortChange = ({ prop, order }) => {
  sortField.value = prop
  sortOrder.value = order
  fetchProducts()
}

// Обработчик изменения фильтров
const applyFilters = () => {
  fetchProducts()
}

// Устанавливаем начальный диапазон при монтировании
onMounted(async () => {
  await setInitialPriceRange()
})

// Ограничиваем priceRange при изменении
watch(priceRange, () => {
  constrainPriceRange()
})
</script>

<style scoped>
.products-table {
  padding: 20px;
}
.charts {
  margin-bottom: 20px;
}
.filters {
  margin-bottom: 20px;
}
canvas {
  max-height: 300px;
}
</style>