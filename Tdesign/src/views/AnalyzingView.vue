<template>
  <div>
    <div id='main' style='width: 700px; height: 600px;'></div>
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
      <RouterLink to='/part34'>Actors</RouterLink>
    </t-button>
  </div>
</template>

<script>
import * as echarts from 'echarts'
import * as Papa from 'papaparse'

export default {
  name: 'Part3View', data() {
    return {
      data: []
    }
  },
  mounted() {
    Papa.parse('src/data/merged_output.csv', {
      download: true,
      header: true,
      complete: (result) => {
        this.data = result.data
        const sourceData = result.data.map(function(row) {
          return [row['score'], row['box'], row['name'], row['year']]
        })

        const chartDom = document.getElementById('main')
        const myChart = echarts.init(chartDom)

        let option = {
          dataset: [{
            source: sourceData
          }],
          title: {
            text: 'Correlation between movie score and box office',
            // subtext: 'By ecStat.regression',
            left: 'center'
          },
          tooltip:{
            trigger:'item',
            formatter: function(params) {
              return 'Name: ' + params.data[2]
              +'<br/>Score: ' + params.data[0]
              +'<br/>Box office: ' + params.data[1]*10 + 'k'
              +'<br/>Time: ' + params.data[3]// 显示第三列的数据，即点的名称
            }
          },
          xAxis: {
            name:'Score',
            axisLabel: {
              interval: 1 // 设置为0表示每个刻度都显示标签
            },
            splitLine: {
              lineStyle: {
                type: 'dashed'
              }
            }
          },
          yAxis: {
            name:'Box Office/thousand Yuan',
            splitLine: {
              lineStyle: {
                type: 'dashed'
              }
            }
          },
          series: [
            {
              color:'darkblue',
              type: 'scatter',
              datasetIndex: 0
            }
          ]
        }
        option && myChart.setOption(option)
      }
    })

  }
}
</script>
<style>
button {
    margin-left: 10px;
  padding: 5px;
}

</style>
