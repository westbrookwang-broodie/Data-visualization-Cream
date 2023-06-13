<template>
  <t-select id="iu" placeholder="最受欢迎" v-model="type" autoWidth @change="icsv2(type)">
    <t-option key="pop" label="最受欢迎" value="most_pop_filmray" />
    <t-option key="score" label="评分最高" value="most_score_filmray" />
  </t-select>
  <div id="main1" style='width: 700px; height: 800px; margin-left: 00px'>
  </div>
</template>


<script>
import {defineComponent} from 'vue'
import * as echarts from 'echarts'
import * as d3 from "d3";
import math from "lodash";

export default {
  name: "RayView",
  data() {
    return {
      type: '',
      mychart: null,
      option: null,
      movie_name: [],
      movies:[],
    }
  },
  methods: {
    async icsv(name1) {
      let this_ = this
      await d3.csv('./src/data/' + name1 + '.csv',function (data1) {
        this_.movie_name.push(data1.movie_title)
        let tmp = {}
        tmp.name = data1.movie_title
        tmp.value = []
        tmp.value.push(data1.movie_points)
        tmp.value.push(data1.movie_long)
        tmp.value.push(data1.movie_points_people)
        tmp.value.push(data1.movie_comments_people)
        tmp.value.push(data1.movie_want_to_see)
        tmp.value.push(data1.movie_have_seen)
        console.log(tmp)
        this_.movies.push(tmp)
      })
      console.log(this.movies)
      // for (let i=0;i<20;i++){
      //   data[i] = data2[i].box;
      //   name[i] = data2[i].name
      // }
    },
    async icsv2(name1) {
      let this_ = this
      this.movie_name = []
      this.movies = []
      await d3.csv('./src/data/' + name1 + '.csv',function (data1) {
        this_.movie_name.push(data1.movie_title)
        let tmp = {}
        tmp.name = data1.movie_title
        tmp.value = []
        tmp.value.push(data1.movie_points)
        tmp.value.push(data1.movie_long)
        tmp.value.push(data1.movie_points_people)
        tmp.value.push(data1.movie_comments_people)
        tmp.value.push(data1.movie_want_to_see)
        tmp.value.push(data1.movie_have_seen)
        console.log(tmp)
        this_.movies.push(tmp)
      })
      console.log("type change")
      console.log(this.movies)

      let selec = {}
      for (let i=0;i<20;i++){
        selec[this.movie_name[i]] = false
      }
      var option

      option = {
        title: {
          text: '电影雷达图',
          style: {
            marginTop: 300
          }
        },
        legend: {
          data: this.movie_name,
          top: "5%",
          selected: selec,
        },
        radar: {
          // shape: 'circle',
          indicator: [
            { name: '电影评分', max: 10 },
            { name: '电影时长', max: 180 },
            { name: '电影评分人数', max: 2200000 },
            { name: '电影评论人数', max: 500000 },
            { name: '电影想看人数', max: 500000 },
            { name: '电影看过人数', max: 4000000 }
          ]
        },
        series: [
          {
            name: '电影雷达分布图',
            type: 'radar',
            data: this.movies,
            top: "10%"
            // selected: {
            //   '霸王别姬': false
            // }
          },
        ]
      };
      this.option = option
      this.option && this.mychart.setOption(this.option);
      // for (let i=0;i<20;i++){
      //   data[i] = data2[i].box;
      //   name[i] = data2[i].name
      // }

    }
  },
  async mounted() {
    var chartDom = document.getElementById('main1');
    var myChart = echarts.init(chartDom);
    this.mychart = myChart
    var option;
    await this.icsv('most_pop_filmray')
    console.log('------------')
    console.log(this.movie_name)

    let selec = {}
    for (let i=0;i<20;i++){
      selec[this.movie_name[i]] = false
    }

    option = {
      title: {
        text: '电影雷达图',
        style: {
          marginTop: 300
        }
      },
      legend: {
        data: this.movie_name,
        top: "5%",
        selected: selec,
      },
      radar: {
        // shape: 'circle',
        indicator: [
          { name: '电影评分', max: 10 },
          { name: '电影时长', max: 160 },
          { name: '电影评分人数', max: 2200000 },
          { name: '电影评论人数', max: 720000 },
          { name: '电影想看人数', max: 900000 },
          { name: '电影看过人数', max: 6000000 }
        ]
      },
      series: [
        {
          name: '电影雷达分布图',
          type: 'radar',
          data: this.movies,
          top: "10%"
          // selected: {
          //   '霸王别姬': false
          // }
        },
      ]
    };
    this.option = option
    option && myChart.setOption(option);
  }
}

// async function icsv(name) {
//   await d3.csv('./src/data/' + name + '.csv',function (data1) {
//     data1.movie_vote_var *= 100
//     data2.push(data1)
//   })
//   data2.sort((a, b)=>{
//     return +b.movie_vote_var - +a.movie_vote_var
//   })
//   data2 = data2.slice(0,168)
//   data2.sort(randomsort)
//   // for (let i=0;i<20;i++){
//   //   data[i] = data2[i].box;
//   //   name[i] = data2[i].name
//   // }
// }
</script>

<style>

</style>
