<template>
  <div>
    <div id='main' style='width: 1200px; height: 500px;'></div>
  </div>

</template>

<script lang='ts'>
import * as echarts from 'echarts'
import * as Papa from 'papaparse'

export default {
  name: 'Part31View',
  data() {
    let xAxisData: string[] = []
    let data1: number[] = []
    let data2: number[] = []
    let data3: number[] = []

    const emphasisStyle = {
      itemStyle: {
        shadowBlur: 100,
        shadowColor: 'rgba(0,0,0,0.3)'
      }
    }
    return {
      data:[],
      xAxisData,
      data1,
      data2,
      data3,
      emphasisStyle
    }
  },

  mounted() {
    Papa.parse('src/data/year_result.csv', {
      download: true,
      header: true,
      complete: (result) => {
        this.xAxisData = result.data.map(row => row['year']);
        this.data1 =  result.data.map(row => row['box']);
        this.data2 = result.data.map(row => row['times']);
        this.data3 = result.data.map(row => row['times1'])
        const chartDom = document.getElementById('main')!
        const myChart = echarts.init(chartDom)
        let option = {
          legend: {
            data: ['Frequency(/Year)', 'Box office (100 million yuan) ',' Popular film frequency'],
            left: '10%'
          },
          title:{
            text:"The effect of the year on the box office of a film",
            left: 'center'
          },
          brush: {
            toolbox: ['rect', 'polygon', 'lineX', 'lineY', 'keep', 'clear'],
            xAxisIndex: 0
          },
          toolbox: {
            feature: {
              magicType: {
                type: ['stack']
              },
              dataView: {}
            }
          },
          tooltip: {
          },
          xAxis: {
            data: this.xAxisData,
            name: 'Year',
            axisLine: { onZero: true },
            splitLine: { show: false },
            splitArea: { show: false }
          },
          yAxis: {
            name: ''
          },
          grid: {
            bottom: 100
          },
          series: [
            {
              name: 'Frequency(/Year)',
              type: 'bar',
              stack: 'one',
              emphasis: this.emphasisStyle,
              data: this.data2,
            },
            {
              name: 'Box office (100 million yuan)',
              type: 'bar',
              stack: 'one',
              emphasis: this.emphasisStyle,
              data: this.data1,
            },
            {
              name: 'Popular film frequency',
              type: 'line',
              emphasis: this.emphasisStyle,
              data: this.data3
            }
          ]
        }

        myChart.on('brushSelected', function(params: any) {
          const brushed = []
          const brushComponent = params.batch[0]

          for (let sIdx = 0; sIdx < brushComponent.selected.length; sIdx++) {
            const rawIndices = brushComponent.selected[sIdx].dataIndex
            brushed.push('[Series ' + sIdx + '] ' + rawIndices.join(', '))
          }

        })
        option && myChart.setOption(option)
      }
    })
  }
}
</script>







