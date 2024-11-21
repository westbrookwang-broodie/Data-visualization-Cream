<template>
  <div style="margin-left: -50px;">
    <h2 style="left: 40%;margin-bottom: 50px;font-weight: bold; font-style: italic">The director's influence on the film</h2>
    <div style="display: flex; margin-bottom: 100px">

      <div id='main0' style='width: 500px; height: 500px; margin-top: 100px'></div>
      <div style="width: 900px;">
        <div id='main1' style='width: 800px; height: 350px;'></div>
        <div style="margin-left: 70px;font-size: 16px;line-height: 2;width: 700px">
          &nbsp;&nbsp;&nbsp;&nbsp;
          By analyzing the frequency and ratings of directors in 200 popular movies, we get the pie chart and line chart above.
          <br/>
          &nbsp;&nbsp;&nbsp;&nbsp;
          Looking at the pie chart, it's easy to see that only a handful of directors are able to produce a large number of popular films at high quality,
          Among them, the most prominent directors are Zhang Yimou, Stephen Chow, Ning Hao, Feng Xiaogang and other household names.
          Most directors have only one or two critically acclaimed films.
          <p/>
          &nbsp;&nbsp;&nbsp;&nbsp;
          The line chart data is closely connected with the pie chart, and we can intuitively find the average score of the corresponding director's popular works in the line chart through the pie chart.
          Through observation, we can intuitively find that the frequency line in the line chart has no obvious relationship with the average line.
        </div>
      </div>
    </div>


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
            text: 'The 200 most popular films - Director pie chart',
            left: 'center',
            textStyle: {
              color: 'gray'
            }
          },
          tooltip: {
            trigger: 'item',
            position: 'right',
            formatter: (params) => {
              return this.data11[params.dataIndex] + ' popular movie: <br/>' +
                'Frequency: ' + this.data21[params.dataIndex] + '<br/>' +
                'Percentage: ' + this.data41[params.dataIndex] + '%<br/>' +
                'Director list: ' + this.data31[params.dataIndex]
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
                  return this.data11[params.dataIndex] + ' Movies'
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
            data: ['Frequency', 'Avg Score'],
            left: '10%'
          },
          title: {
            text: "Director's film frequency and average rating",
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
            name: 'Year',
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
              name: 'Frequency',
              type: 'line',
              data: this.frequency
            },
            {
              name: 'Avg Score',
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