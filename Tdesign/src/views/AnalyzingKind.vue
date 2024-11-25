<template>
  <div>

    <div style="display: flex">
      <div id='main1' style='width:700px;height: 700px;'></div>
      <div style='width: 400px;margin-top: 150px;font-size: 16px;line-height: 2'>
        &nbsp;&nbsp;&nbsp;&nbsp;
        By analyzing the categories of the 200 most popular movies in China (each movie may belong to multiple categories),
        we found that drama, comedy, action, and romance films are widely loved and recognized in the Chinese market, followed by fantasy, crime, and suspense categories.
        <br/>
        &nbsp;&nbsp;&nbsp;&nbsp;
        If you want to create a well-received and audience-recognized movie, you can focus on researching these categories.
      </div>
    </div>

    <div>
      <h2 style="font-weight: bold; font-style: italic; left: 40%">Case Study: Movie Categories and Feature Analysis</h2>
      <div style="left:25%; margin-top: 20px;font-size: 16px;line-height: 2">
        We conducted simple classifications and measurements for the following forty movies. These analyses are presented in the form of relationship charts and radar charts.
      </div>
      <div style="margin-left: -150px">
        <RelationChart></RelationChart>
      </div>
      <div style="display:flex;">
        <RayView></RayView>
        <div style="font-size: 16px;line-height: 2; width: 400px; margin-left: 50px; margin-top: 150px">

          <p> &nbsp;&nbsp;&nbsp;&nbsp;
            The above forty movies were selected from the twenty most popular movies and the twenty highest-rated movies. By classifying these films, we created the relationship chart shown above.
            Observing these data, we found that these forty movies share strong commonalities with the categories analyzed in the pie chart on this page—mostly dramas and romances, with fewer biographical and sci-fi films.</p>
          <br/>
          <p> &nbsp;&nbsp;&nbsp;&nbsp;To further explore the features of these movies, we created radar charts for each one, using six different dimensions—movie rating, number of viewers, number of people interested in watching, number of comments, number of raters, and movie duration—
            to measure the quality of a movie. Users can select their movies of interest to compare across these dimensions and draw their own conclusions.</p>
        </div>
      </div>

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

<script>
import * as echarts from 'echarts'
import * as Papa from 'papaparse'
import RelationChart from '@/views/RelationChart.vue'
import RayView from "@/views/RayView.vue";

export default {
  name: 'Part32View',
  components: {RayView, RelationChart},
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
              radius: ['20%', '70%'],
              center: ['50%', '50%'],
              data: this.data2,
              roseType: 'radius',
              label: {
                formatter: (params) => {
                  return this.data1[params.dataIndex];
                },
                fontSize: 15,
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
                length: 1,
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
