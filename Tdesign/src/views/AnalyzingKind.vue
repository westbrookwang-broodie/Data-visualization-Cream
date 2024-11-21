<template>
  <div>
    <div id='main1' style='width: 700px; height: 800px;'></div>
    <RelationChart></RelationChart>
    <t-button ghost shape="round"
              size="large">
      <RouterLink to='/part31'>Year</RouterLink>
    </t-button>
    <t-button ghost shape="round"
              size="large">
      <RouterLink to='/part32'>Theme</RouterLink>
    </t-button>
    <t-button ghost shape="round"
              size="large">
      <RouterLink to='/part33'>Director</RouterLink>
    </t-button>
    <t-button ghost shape="round"
              size="large">
      <RouterLink to='/part34'>Actor</RouterLink>
    </t-button>
  </div>
</template>

<script>
import * as echarts from 'echarts'
import * as Papa from 'papaparse'
import RelationChart from '@/views/RelationChart.vue'
  export default {
  name: 'Part32View',
  components: { RelationChart},
  data() {
    return {
      data1:[],
      data2:[],
      data3:[],
      data4:[],
    }
  },
  mounted() {
    Papa.parse('src/data/kind_result.csv', {
      download: true,
      header: true,
      complete: (result) => {
        this.data1 = result.data.map(row => row['类型'])
        this.data2 = result.data.map(row => row['频次'])
        console.log(this.data2)
        this.data3 = result.data.map(row => row['平均评分'])
        this.data4 = result.data.map(row => row['百分比'])

        const chartDom = document.getElementById('main1')
        const myChart = echarts.init(chartDom)

        let option = {
          title: {
            text: 'Top 200 popular movie types',
            left: 'center'
          },
          tooltip: {
            trigger: 'item',
            formatter: (params) => {
              return this.data1[params.dataIndex] + ': <br/>' +
                'Frequency: ' + this.data2[params.dataIndex] + '<br/>'+
                'Percentage: '+ this.data4[params.dataIndex] + '%<br/>'+
                'Avg Score: ' + this.data3[params.dataIndex];
            },
          },
          legend: {
            orient: 'vertical',
            left: 'left'
          },
          series: [
            {
              name: 'Access From',
              type: 'pie',
              radius: '50%',
              data:this.data2,
              label: {
                formatter: (params) => {
                  return this.data1[params.dataIndex];
                },
                rich: {
                  b: {
                    fontWeight: 'bold',
                    lineHeight: 18
                  }
                }
              },
              emphasis: {
                itemStyle: {
                  shadowBlur: 10,
                  shadowOffsetX: 0,
                  shadowColor: 'rgba(0, 0, 0, 0.5)'
                }
              }
            }
          ]
        }

        option && myChart.setOption(option)
      }
    })

  }
}
</script>

<style scoped>

</style>
