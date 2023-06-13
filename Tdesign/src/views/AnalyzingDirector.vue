<template>
  <div style="margin-left: -50px;">
    <h2 style="left: 40%;margin-bottom: 50px;font-weight: bold; font-style: italic">导演对电影的影响</h2>
    <div style="display: flex; margin-bottom: 100px">

      <div id='main0' style='width: 500px; height: 500px;'></div>
      <div style="width: 900px;">
        <div id='main1' style='width: 800px; height: 350px;'></div>
        <div style="margin-left: 80px">
          通过分析两百部受欢迎电影中导演的出现频次及评分，我们得到了以上两幅图。
        </div>
      </div>
    </div>

    <h2 style="left: 40%;margin-bottom: 50px;font-weight: bold; font-style: italic">演员对电影的影响</h2>
    <Part34View></Part34View>
  </div>

</template>

<script>
import * as echarts from 'echarts'
import * as Papa from 'papaparse'
import Part34View from "@/views/AnalyzingActor.vue";

export default {
  name: 'Part33View',
  components: {Part34View},
  data() {
    return {
      director: [],
      frequency: [],
      score: [],
      data11: [],
      data21: [],
      data31: [],
      data41: []
    }
  },
  mounted() {
    Papa.parse('src/data/director_result1.csv', {
      download: true,
      header: true,
      complete: (result) => {
        this.data11 = result.data.map(row => row['数量'])
        this.data21 = result.data.map(row => row['频次'])
        this.data31 = result.data.map(row => row['导演'])
        this.data41 = result.data.map(row => row['百分比'])

        const chartDom1 = document.getElementById('main0')
        const myChart1 = echarts.init(chartDom1)

        let option1 = {
          title: {
            text: '最受欢迎的两百部电影——导演分布饼图',
            left: 'center',
            textStyle: {
              color: 'gray'
            }
          },
          tooltip: {
            trigger: 'item',
            position: 'right',
            formatter: (params) => {
              return this.data11[params.dataIndex] + '部受欢迎电影: <br/>' +
                '频次: ' + this.data21[params.dataIndex] + '<br/>' +
                '百分比: ' + this.data41[params.dataIndex] + '%<br/>' +
                '导演名单: ' + this.data31[params.dataIndex]
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
              radius: ['40%', '70%'],
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
    Papa.parse('src/data/director_result.csv', {
      download: true,
      header: true,
      complete: (result) => {
        this.director = result.data.map(row => row['导演'])
        this.frequency = result.data.map(row => row['频次'])
        this.score = result.data.map(row => row['平均评分'])

        const chartDom2 = document.getElementById('main1')
        const myChart2 = echarts.init(chartDom2)

        let option2 = {
          legend: {
            data: ['频次', '平均评分'],
            left: '10%'
          },
          title: {
            text: "导演电影频次及平均评分统计图",
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
            data: this.director,
            name: '年',
            axisLine: {onZero: true},
            splitLine: {show: false},
            splitArea: {show: false}
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
