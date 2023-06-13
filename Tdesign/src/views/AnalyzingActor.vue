<template>
  <div>
    <div style="display: flex">
      <div id='main2' style='width: 500px; height: 500px;'></div>
      <div style=";font-size: 16px;line-height: 2;width: 700px; margin-top: 100px; margin-left: 70px">
        &nbsp;&nbsp;&nbsp;&nbsp;
        对同一样本以演员为研究对象进行以上相同的分析，我们可以得到相同样式的两组图。
        <br/>
        &nbsp;&nbsp;&nbsp;&nbsp;
        观察饼状图我们可以发现，部分演员频繁主演了广受认可的电影，如徐峥，黄渤，邓超，周星驰等，也有演员就在这些电影中昙花一现，从此销声匿迹。
        优秀电影的背后必然有演员的演技支持，而这些电影也反向提高了演员的知名度和影响力，给予他们更多参演电影的机会。
        <p/>
        &nbsp;&nbsp;&nbsp;&nbsp;
        折线图数据与饼状图紧密相连，我们可以通过饼状图很直观地在折线图中找到对应演员受欢迎作品的平均评分。
        通过观察我们可以很直观地发现，折线图中的频率折线与平均分折线依旧并无明显关系。如，邓超虽然频繁出现在受欢迎电影中，他的平均评分却只有6分左右。

      </div>
    </div>

    <div id='main3' style='margin-left:-50px;width: 1500px; height: 400px'></div>
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
<!--    <t-button ghost shape="round"-->
<!--              size="large">-->
<!--      <RouterLink to='/part34'>演员</RouterLink>-->
<!--    </t-button>-->
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
            text: '最受欢迎的两百部电影——演员分布饼图',
            left: 'center',
            textStyle: {
              color: 'gray'
            }
          },
          tooltip: {
            trigger: 'item',
            position:'right',
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
              radius: ['40%','70%'],
              data: this.data21,
              itemStyle: {
                borderRadius: 10,
                borderColor: '#fff',
                borderWidth: 2
              },
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
            text:"演员电影频次及平均评分统计图",
            left: 'center',
            textStyle: {
              color: 'gray'
            }
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
            trigger: 'axis'
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
