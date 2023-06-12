<template>
  <div style="display: flex">
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
        <RouterLink to='/part33'>人员</RouterLink>
      </t-button>
<!--      <t-button ghost shape="round"-->
<!--                size="large">-->
<!--        <RouterLink to='/part34'>演员</RouterLink>-->
<!--      </t-button>-->
    </div>
    <div style='width: 500px;margin-top: 100px;font-size: 16px;line-height: 2'>
      &nbsp;&nbsp;&nbsp;&nbsp;
      散点图将带你进入电影票房与评分之间微妙关系的世界，揭示出观众对电影质量与商业成功的综合评价。
      <br/>
      &nbsp;&nbsp;&nbsp;&nbsp;
      每个散点代表着一部电影，横坐标表示电影的评分，纵坐标表示电影的票房。通过观察散点的分布情况，你将发现一些有趣的模式和趋势。
      有时，高票房与高评分相辅相成，彰显出一部优质电影的双重成功；而有时，也会出现票房大卖却饱受差评的情况，引发对观众口味和市场营销的思考。
      这个散点图的深度分析将帮助你了解观众对电影品质和商业价值的综合考量，以及为何某些电影能够在票房与评分上取得双重胜利。
      通过透视这种复杂的关系，我们将更好地理解电影行业的商业机制和观众的喜好趋势，从而为未来的电影创作和市场策略提供更深入的洞察。
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
