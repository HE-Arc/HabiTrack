<template>
  <Bar id="my-chart-id" ref="chart" :options="chartOptions" :data="chartData" />
</template>

<script>
import { Bar } from "vue-chartjs";
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  BarElement,
  CategoryScale,
  LinearScale,
} from "chart.js";

ChartJS.register(Title, Tooltip, BarElement, CategoryScale, LinearScale);

export default {
  props: {
    propEntries: {
      type: Array,
      required: true,
    },
    propTemplate: {
      type: Object,
    },
  },
  name: "BarChart",
  components: { Bar },
  computed: {
    chartData() {
      return {
        labels: this.propEntries.map((entry) =>
          this.formatDate(entry.created_at)
        ),
        datasets: [
          {
            data: this.getEntries(),
            backgroundColor: ["rgba(255, 255, 255, 0.8)"],
            label: "Last 10 entries",
          },
        ],
      };
    },
    chartOptions() {
      return {
        responsive: true,
      };
    },
  },
  methods: {
    formatDate(dateString) {
      const date = new Date(dateString);
      const options = { year: "numeric", month: "short", day: "numeric" };
      return date.toLocaleDateString("en-US", options);
    },
    // last 10 entries
    getEntries() {
      //   let templateOptions = [ // TODO MAYBE ANOTHER DAY
      //     this.propTemplate.option_1,
      //     this.propTemplate.option_2,
      //     this.propTemplate.option_3,
      //     this.propTemplate.option_4,
      //     this.propTemplate.option_5,
      //   ];
      return this.propEntries.map((entry) => entry.selected_option);
    },
  },
};
</script>
