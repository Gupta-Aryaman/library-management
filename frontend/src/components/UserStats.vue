<template>
    <UserHeader />
    <div v-if="dataLoaded">

      <div class="d-flex justify-content-center align-items-center mt-5 mb-5">
            <h1>All time User Stats</h1>
        </div>

        <div class="row mx-5">
            <div class="col-sm-6 mb-3 mb-sm-0">
                <PieChart v-if="pieDataReady" :title="pieTitle" :labels="pieLabels" :data="pieData" />
            </div>
            <div class="col-sm-6">
                <BarChart v-if="barDataReady" :title="barTitle" :labels="barLabels" :data="barData" />
            </div>
            
        </div>
    </div>

  </template>
  
  <script>
  import UserHeader from './UserHeader.vue';
  import BarChart from './BarChart.vue';
  import PieChart from './PieChart.vue';
  
  export default {
    name: 'UserStats',
    components: {
      UserHeader,
      BarChart,
      PieChart
    },
    data() {
      return {
        dataLoaded: false,
        pieDataReady: false,
        barDataReady: false,
        pieTitle: "Section Distribution",
        barTitle: "Books Read",
        pieLabels: [],
        pieData: [],
        barLabels: [],
        barData: []
      }
    },
    mounted() {
      this.fetchStats();
    },
    methods: {
      fetchStats() {
        const myHeaders = new Headers();
        myHeaders.append("Authorization", "Bearer " + localStorage.getItem('user_token'));
  
        const requestOptions = {
          method: "GET",
          headers: myHeaders,
          redirect: "follow"
        };
  
        fetch("http://localhost:5000/fetch_stats", requestOptions)
          .then(response => response.json())
          .then(data => {
            this.pieLabels = data.pie_sections;
            this.pieData = data.pie_counts;
            this.barLabels = data.bar_months;
            this.barData = data.bar_counts;

            this.dataLoaded = true;
            this.pieDataReady = true;
            this.barDataReady = true;
          })
          .catch(error => {
            console.error(error);
            // Handle error
          });
      }
    }
  }
  </script>
  