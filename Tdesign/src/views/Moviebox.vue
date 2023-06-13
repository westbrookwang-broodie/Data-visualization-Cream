<template>
  <div style="display: flex">
    <div id="atlasMain" style="width: 800px;"></div>
    <div style='width:400px;margin-top: 100px;font-size: 16px;line-height: 2'>
      <p>
      &nbsp;&nbsp;&nbsp;&nbsp;
      时光如梭，而电影票房的动态却凝聚着岁月的痕迹。在这个页面上，我们带你踏上一段时间之旅，从2000年到2022年，
      探索每年的前几名电影票房。</p>
      <br/>
      <p>
      &nbsp;&nbsp;&nbsp;&nbsp;
      这个动态图将展示着过去二十多年中每年票房冠军的电影，让你亲眼目睹经典之作的辉煌崛起。
      透过数据的视角，你将发现票房的起伏和变化，揭示出影响力瞬息万变的电影市场。无论是商业大片的崛起，还是突破性的独立电影，
      这个动态图将带你领略电影票房的壮丽风景线，并让你更加了解电影产业的发展历程和成功之道。</p>
    </div>
  </div>
</template>
<style scoped>
#atlasMain{
    width:800px;
    height:600px;
    margin-left: 30px;
}
</style>
<script>
import * as echarts from 'echarts';
import * as d3 from "d3";
var data = []
var name = []
var option
var data2 = []
var myChart

var year = 2000

export default {
  name: "index",
  data() {
    return {
      data: []
    }

  },
  created() {
    this.$nextTick(function () {
      this.initChart()
    })
  },
  methods: {
    initChart() {
      var chartDom = document.getElementById('atlasMain');
      myChart = echarts.init(chartDom);
      // var option;
      icsv(2000)
      // const data = [];
      option = {
        xAxis: {
          max: 'dataMax'
        },
        yAxis: {
          type: 'category',
          data: name,
          inverse: true,
          animationDuration: 300,
          animationDurationUpdate: 300,
          max: 6 // only the largest 3 bars will be displayed
        },
        series: [
          {
            realtimeSort: true,
            name: 'X',
            type: 'bar',
            data: data,
            label: {
              show: true,
              position: 'right',
              valueAnimation: true
            }
          }
        ],
        graphic: {
          elements: [
            {
              type: 'text',
              right: 160,
              bottom: 60,
              style: {
                text: year,
                font: 'bolder 80px monospace',
                fill: 'rgba(100, 100, 100, 0.25)'
              },
              z: 100
            }
          ]
        },
        legend: {
          show: true
        },
        animationDuration: 0,
        animationDurationUpdate: 3000,
        animationEasing: 'linear',
        animationEasingUpdate: 'linear'
      };
      async function icsv(year) {
        const d = []
        await d3.csv('./src/data/movie'+ year.toString()+'box.csv',function (data1) {
          data2.push(data1)
        })
        data2.sort((a, b)=>{
          return +b.box - +a.box
        })
        data2 = data2.slice(0,20)
        for (let i=0;i<20;i++){
          data[i] = data2[i].box;
          name[i] = data2[i].name
        }
      }

      function run() {
        icsv(year+1)
        if (year <2022) {
          year +=1
        }
        // for (var i = 0; i < data.length; ++i) {
        //   if (Math.random() > 0.9) {
        //     data[i] += Math.round(Math.random() * 2000);
        //   } else {
        //     data[i] += Math.round(Math.random() * 200);
        //   }
        // }
        option.graphic.elements[0].style.text = (year).toString();
        myChart.setOption(option)
        myChart.setOption({
          yAxis: {
            data: name,
          },
          series: [
            {
              type: 'bar',
              data
            }
          ],
        });

      }
      setTimeout(function () {
        run();

      }, 0);
      setInterval(function () {
        run();
        console.log(data)
        console.log(name)
      }, 1000);
      option && myChart.setOption(option);
    },
  }
}
</script>


