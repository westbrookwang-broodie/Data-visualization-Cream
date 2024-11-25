<template>
  <div style="margin-bottom: 10px">
    <div id='main' style='width: 1200px; height: 500px;'></div>
    <div style='font-size: 16px;line-height: 2;margin-bottom: 60px; width: 1000px; margin-left: 5%'>
      &nbsp;&nbsp;&nbsp;&nbsp;
      Based on the available data, we have generated the above bar chart illustrating the impact of years on movie box office performance.
      The horizontal axis represents the years, while the vertical axis uses different colors and styles to indicate three sets of data: movie frequency, total box office revenue, and frequency of popular movies.
      <br/>
      &nbsp;&nbsp;&nbsp;&nbsp;
      Observing the chart, we find that the Chinese film market experienced significant growth from 2000 to 2019, with substantial increases in movie frequency and box office revenue, indicating an upward trend overall.
      However, from 2020 to 2022, the market entered a period of decline. This downturn is closely linked to the impact of the COVID-19 pandemic.
      It is believed that the movie market will recover rapidly after overcoming this crisis.
    </div>
    <t-button ghost shape="round"
              size="large">
      <RouterLink to='/part31'>Year</RouterLink>
    </t-button>
    <t-button ghost shape="round"
              size="large">
      <RouterLink to='/part32'>Genre</RouterLink>
    </t-button>
    <t-button ghost shape="round"
              size="large">
      <RouterLink to='/part33'>Personnel</RouterLink>
    </t-button>
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
            data: ['频次（/年）', '票房（亿元）','受欢迎电影频次'],
            left: '10%'
          },
          title:{
            text:"年份对电影票房的影响",
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
            name: '年',
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
              name: '频次（/年）',
              type: 'bar',
              stack: 'one',
              emphasis: this.emphasisStyle,
              data: this.data2,
            },
            {
              name: '票房（亿元）',
              type: 'bar',
              stack: 'one',
              emphasis: this.emphasisStyle,
              data: this.data1,
            },
            {
              name: '受欢迎电影频次',
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







