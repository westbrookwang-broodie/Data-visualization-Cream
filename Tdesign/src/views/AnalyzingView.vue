<template>
  <div style="display: flex">
    <div>
      <div id='main' style='width: 700px; height: 600px;'></div>
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
      <!-- Uncomment the following block if "Actors" is required -->
      <!--
      <t-button ghost shape="round"
                size="large">
        <RouterLink to='/part34'>Actors</RouterLink>
      </t-button>
      -->
    </div>
    <div style='width: 500px;margin-top: 100px;font-size: 16px;line-height: 2'>
      &nbsp;&nbsp;&nbsp;&nbsp;
      The scatter plot takes you into the intricate world of the relationship between movie box office performance and ratings, revealing a combined evaluation of quality and commercial success.
      <br/>
      &nbsp;&nbsp;&nbsp;&nbsp;
      Each dot represents a movie, with the horizontal axis indicating the rating and the vertical axis representing the box office revenue. By observing the distribution of the dots, you will uncover fascinating patterns and trends.
      Sometimes, high box office and high ratings go hand in hand, showcasing a movie's dual success. Other times, a blockbuster may face poor reviews, prompting reflections on audience preferences and marketing strategies.
      This scatter plot's in-depth analysis helps you understand the audience's comprehensive consideration of movie quality and commercial value, and why some films achieve dual triumphs in both box office and ratings.
      By exploring this complex relationship, we can better comprehend the commercial mechanisms of the film industry and audience preference trends, providing deeper insights for future film creation and marketing strategies.
    </div>
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
        const sourceData = result.data.map(function (row) {
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
          tooltip: {
            trigger: 'item',
            formatter: function (params) {
              return '名称: ' + params.data[2]
                + '<br/>评分: ' + params.data[0]
                + '<br/>票房: ' + params.data[1] + '万'
                + '<br/>时间: ' + params.data[3]// 显示第三列的数据，即点的名称
            }
          },
          xAxis: {
            name: '评分/分',
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
            name: '票房/万元',
            splitLine: {
              lineStyle: {
                type: 'dashed'
              }
            }
          },
          series: [
            {
              color: 'darkblue',
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
