<template>
  <div>
    <div id='main' style='width: 700px; height: 600px;'></div>
    <t-button ghost shape="round"
              size="large">
      <RouterLink to='/part31'>年份</RouterLink>
    </t-button>
    <t-button ghost shape="round"
              size="large">
      <RouterLink to='/part32'>题材</RouterLink>
    </t-button>
    <t-button ghost shape="round"
              size="large">
      <RouterLink to='/part33'>导演</RouterLink>
    </t-button>
    <t-button ghost shape="round"
              size="large">
      <RouterLink to='/part34'>演员</RouterLink>
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
            text: '电影评分票房关系图',
            // subtext: 'By ecStat.regression',
            left: 'center'
          },
          tooltip:{
            trigger:'item',
            formatter: function(params) {
              return '名称: ' + params.data[2]
              +'<br/>评分: ' + params.data[0]
              +'<br/>票房: ' + params.data[1] + '万'
              +'<br/>时间: ' + params.data[3]// 显示第三列的数据，即点的名称
            }
          },
          xAxis: {
            name:'评分/分',
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
            name:'票房/万元',
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
