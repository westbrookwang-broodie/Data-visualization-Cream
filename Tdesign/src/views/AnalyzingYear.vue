<template>
  <div style="margin-bottom: 10px">
    <div id='main' style='width: 1200px; height: 500px;'></div>
    <div style='font-size: 16px;line-height: 2;margin-bottom: 60px'>
      &nbsp;&nbsp;&nbsp;&nbsp;
      根据已知数据，我们生成了如上关于年份对电影票房影响的柱状图。
      横坐标表示了年份，纵坐标则利用不同色彩和形式表示了电影频次，电影总票房，受欢迎电影频次三组数据。
      <br/>
      &nbsp;&nbsp;&nbsp;&nbsp;
      通过观察我们发现，自2000-2019年中国电影市场整体升幅较大,电影频次及票房基数都有显著的提升，整体趋势向上。
      然而，2020年-2022年，电影市场却出现了低迷期。这样的低迷与新型冠状病毒疫情造成的种种打击密不可分。
      相信度过危机后的电影市场将迅速恢复。

    </div>
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
      <RouterLink to='/part33'>人员</RouterLink>
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







