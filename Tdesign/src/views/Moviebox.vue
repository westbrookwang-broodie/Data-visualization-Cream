<template>
  <div style="display: flex">
    <div id="atlasMain" style="width: 800px;"></div>
    <div style='width:400px;margin-top: 100px;font-size: 16px;line-height: 2'>
      <p>
        &nbsp;&nbsp;&nbsp;&nbsp;
        Time flies, but the dynamics of box office revenues capture the traces of the years. On this page, we take you on a journey through time, from 2000 to 2022,
        exploring the top box office hits of each year.</p>
      <br/>
      <p>
        &nbsp;&nbsp;&nbsp;&nbsp;
        This dynamic chart showcases the box office champions of the past two decades, allowing you to witness the rise of classic masterpieces.
        Through the lens of data, you will observe the ebb and flow of box office trends, revealing the ever-changing influences in the movie market.
        Whether it's the rise of blockbuster films or groundbreaking independent productions, this chart offers a stunning panorama of box office achievements,
        providing insights into the evolution of the film industry and the paths to success.</p>
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


