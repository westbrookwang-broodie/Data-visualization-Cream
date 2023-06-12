<template>
  <div>
    <div style="display: flex">
    <div id='main1' style='width:800px;height: 800px;'></div>
    <div style='width: 500px;margin-top: 100px;font-size: 16px;line-height: 2'>
      通过分析中国最受欢迎的两百部电影的所属类别情况（每部电影可归属多个类别），
      我们发现剧情，喜剧，动作，爱情类的电影在中国市场受到了十分广泛的喜爱和认同，其次是奇幻、犯罪、悬疑类别的电影。
      <br/>
      如果想制作一部口碑良好，受观众认可的电影，可以从以上的几个类别入手研究。
    </div>
    </div>
    <RelationChart></RelationChart>
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
import RelationChart from '@/views/RelationChart.vue'

export default {
  name: 'Part32View',
  components: {RelationChart},
  data() {
    return {
      data1: [],
      data2: [],
      data3: [],
      data4: [],
    }
  },
  mounted() {
    Papa.parse('src/data/kind_result.csv', {
      download: true,
      header: true,
      complete: (result) => {
        this.data1 = result.data.map(row => row['类型'])
        this.data2 = result.data.map(row => row['频次'])
        console.log(this.data2)
        this.data3 = result.data.map(row => row['平均评分'])
        this.data4 = result.data.map(row => row['百分比'])

        const chartDom = document.getElementById('main1')
        const myChart = echarts.init(chartDom)
        let option = {
          title: {
            text: '最受欢迎的两百部电影题材分布饼图',
            left: 'center',
            top: 20,
          },

          tooltip: {
            trigger: 'item',
            formatter: (params) => {
              return this.data1[params.dataIndex] + ': <br/>' +
                '频次: ' + this.data2[params.dataIndex] + '<br/>' +
                '百分比: ' + this.data4[params.dataIndex] + '%<br/>' +
                '平均分: ' + this.data3[params.dataIndex];
            },
          },
          visualMap: {
            show: false,
            min: 0,
            max: 150,
            inRange: {
              colorLightness: [0, 1]
            }
          },
          series: [
            {
              name: 'Access From',
              type: 'pie',
              radius: ['25%', '80%'],
              center: ['50%', '50%'],
              data: this.data2,
              roseType: 'radius',
              label: {
                formatter: (params) => {
                  return this.data1[params.dataIndex];
                },
                fontSize:15,
                rich: {
                  b: {
                    fontWeight: 'bold',
                    lineHeight: 18
                  }
                }
              },
              labelLine: {
                lineStyle: {
                  color: 'gray'
                },
                smooth: 0.2,
                length: 10,
                length2: 20
              },
              itemStyle: {
                color: '#134236',
                shadowBlur: 200,
                shadowColor: 'rgba(0, 0, 0, 0)'
              },

              animationType: 'scale',
              animationEasing: 'elasticOut',
              animationDelay: function (idx) {
                return Math.random() * 200;
              }
            }
          ]
        };


        // let option = {
        //   title: {
        //     text: 'Referer of a Website',
        //     subtext: 'Fake Data',
        //     left: 'center'
        //   },
        //   tooltip: {
        //     trigger: 'item',
        //     formatter: (params) => {
        //       return this.data1[params.dataIndex] + ': <br/>' +
        //         '频次: ' + this.data2[params.dataIndex] + '<br/>'+
        //         '百分比: '+ this.data4[params.dataIndex] + '%<br/>'+
        //         '平均分: ' + this.data3[params.dataIndex];
        //     },
        //   },
        //   legend: {
        //     orient: 'vertical',
        //     left: 'left'
        //   },
        //   series: [
        //     {
        //       name: 'Access From',
        //       type: 'pie',
        //       radius: '50%',
        //       data:this.data2,
        //       label: {
        //         formatter: (params) => {
        //           return this.data1[params.dataIndex];
        //         },
        //         rich: {
        //           b: {
        //             fontWeight: 'bold',
        //             lineHeight: 18
        //           }
        //         }
        //       },
        //       emphasis: {
        //         itemStyle: {
        //           shadowBlur: 10,
        //           shadowOffsetX: 0,
        //           shadowColor: 'rgba(0, 0, 0, 0.5)'
        //         }
        //       }
        //     }
        //   ]
        // }

        option && myChart.setOption(option)
      }
    })

  }
}
</script>

<style scoped>

</style>
