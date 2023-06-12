<template>
  <div>
    <p>This is Part34</p>
    <div id='main2' style='width: 700px; height: 800px;'></div>
    <div id='main3' style='width: 6000px; height: 800px;'></div>
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
  name: 'Part34View',
  data() {
    return {
      actor:[],
      frequency:[],
      score:[],
      data11: [],
      data21: [],
      data31: [],
      data41: []
    }
  },
  mounted() {
    Papa.parse('src/data/actor_result1.csv', {
      download: true,
      header: true,
      complete: (result) => {
        this.data11 = result.data.map(row => row['数量'])
        this.data21 = result.data.map(row => row['频次'])
        this.data31 = result.data.map(row => row['人员'])
        this.data41 = result.data.map(row => row['百分比'])

        const chartDom1 = document.getElementById('main2')
        const myChart1 = echarts.init(chartDom1)

        let option1 = {
          title: {
            text: 'Referer of a Website',
            subtext: 'Fake Data',
            left: 'center'
          },
          tooltip: {
            trigger: 'item',
            formatter: (params) => {
              return this.data11[params.dataIndex] + '部受欢迎电影: <br/>' +
                '频次: ' + this.data21[params.dataIndex] + '<br/>' +
                '百分比: ' + this.data41[params.dataIndex] + '%<br/>' +
                '名单: ' + this.data31[params.dataIndex]
            }
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
              data: this.data21,
              label: {
                formatter: (params) => {
                  return this.data11[params.dataIndex] + '部'
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

        option1 && myChart1.setOption(option1)
      }
    })
    Papa.parse('src/data/actor_result.csv', {
      download: true,
      header: true,
      complete: (result) => {
        this.actor = result.data.map(row => row['卡司'])
        this.frequency = result.data.map(row => row['频次'])
        this.score = result.data.map(row => row['平均评分'])

        const chartDom2 = document.getElementById('main3')
        const myChart2 = echarts.init(chartDom2)

        let option2 = {
          legend: {
            data: ['频次','平均评分'],
            left: '10%'
          },
          title:{
            text:"导演对电影的影响",
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
            data: this.actor,
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
              name: '频次',
              type: 'line',
              data: this.frequency
            },
            {
              name: '平均评分',
              type: 'line',
              data: this.score
            }
          ]
        }

        option2 && myChart2.setOption(option2)
      }
    })

  }
}
</script>

<style scoped>

</style>
