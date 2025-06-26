<template>
  <div id="app">
    <h1>Товары</h1>
    <products-table />
  </div>
</template>

<script setup>
import ProductsTable from './components/ProductsTable.vue'
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>