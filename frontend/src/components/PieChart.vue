<template>
    <div class="card shadow-sm">
      <div class="card-header">
        <h4 class="card-title text-center">{{ title }}</h4>
      </div>
      <div class="card-body row">
        <Pie
          class="m-auto"
          :data="pieChartData"
          :options="pieChartOptions"
          style="height: 20rem; width: 20rem"
        v-if="pieChartData!=[]"/>
        <div v-else>
          <h3>No data available</h3>
        </div>
      </div>
      <!-- <pre>{{ props }}</pre> -->
    </div>
  </template>
  
  <script>
import { defineProps, toRefs, ref } from 'vue'
import { Pie } from 'vue-chartjs'
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  BarController,
  CategoryScale,
  LinearScale,
  BarElement,
  ArcElement
} from 'chart.js'

ChartJS.register(
  Title,
  Tooltip,
  Legend,
  BarController,
  CategoryScale,
  LinearScale,
  BarElement,
  ArcElement
)

export default {
  props: {
    title: {
      type: String,
      required: true
    },
    labels: {
      type: Array,
      required: true
    },
    data: {
      type: Array,
      required: true
    }
  },
  setup(props) {
    const { title, labels, data } = toRefs(props)

    const pieChartData = ref({
      labels: labels.value,
      datasets: [{
        backgroundColor: [
          '#41B883',
          '#E46651',
          '#00D8FF',
          '#DD1B16',
          '#1E88E5',
          '#FBBC04',
          '#F4511E',
          '#6D4C41',
          '#546E7A',
          '#D32F2F',
          '#7B1FA2',
          '#303F9F',
          '#1976D2',
          '#0288D1',
          '#0097A7',
          '#00796B',
          '#388E3C',
          '#689F38',
          '#AFB42B',
          '#FBC02D'
        ],
        data: data.value
      }]
    })

    const pieChartOptions = ref({
      responsive: true,
      maintainAspectRatio: false
    })

    return { title, pieChartData, pieChartOptions }
  },
  components: {
    Pie
  }
}
</script>

  <style scoped></style>