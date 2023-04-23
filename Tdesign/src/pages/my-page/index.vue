<template>
<!--  <div class="login-wrapper">-->
<!--    <login-header />-->
<!--    <div class="login-container">-->
<!--      <p>My Page</p>-->
<!--      <h1>yuyuyuyuy</h1>-->
<!--      <br>-->
<!--      <h2>TYTYTYTY</h2>-->
  <svg width=600 height=500></svg>
<!--      </div>-->

<!--      <tdesign-setting />-->

<!--    <footer class="copyright">Copyright @ 2021-2022 Tencent. All Rights Reserved</footer>-->
<!--  </div>-->
</template>
<script lang="ts">
import * as d3 from 'd3';
import Papa from 'papaparse';
export default {
  name: 'index',
  data(){
    return{
      data: [],
      data2: []
    }
  },
  methods: {
    async icsv() {
      const d = []
      let this_ = this
      await d3.csv('src/data/movie2000box.csv',function (data1) {
        d.push(+data1['票房（万元）'])
        this_.data2.push(data1['电影'])
      })
      this.data = d
    },
    async draw(){
      await this.icsv()
      let margin = 20;
      let svg = d3.select('svg');
      svg.attr('width',4000);
      svg.attr('height',2000);
      let width = svg.attr('width')
      let height = svg.attr('height')
      let g = svg.append('g')
        .attr("transform", 'translate('+ margin +','+ margin +')');

      // 定义 X 轴比例尺
      let scaleX = d3.scaleBand()
        .domain(d3.range(this.data.length))
        .rangeRound([0,width - margin*2])
        // .tickFormat(d3.format(".0%"));

      // 定义 y 轴比例尺
      let scaleY = d3.scaleLinear()
        .domain([0,d3.max(this.data)])
        .range([height - margin * 2,0]);
      // 上边距30；注意：range 后面跟的参数0，放在第二位 因为 y轴正方向向下

      // 绘制 x y 轴
      let this_ = this;
      let axisX = d3.axisBottom(scaleX).tickFormat(
        (d,i)=>{return this_.data2[i]}
        );
      let axisY = d3.axisLeft(scaleY);
      g.append('g').attr("transform", "translate(0, " + (height - margin * 2) + ")").call(axisX)
      g.append('g').attr("transform", "translate(0,0)").call(axisY);

      let cnt = 0
      setInterval(()=> {
        cnt+=1
        // 改变横坐标下电影标签
          axisX.tickFormat((d,i)=>{
          return this.data2[i]
        })
        g.select('g').transition().duration(500).call(axisX)



      // 创建矩形分组
      const gs = g.selectAll('rect')
        .data(this.data)
        // .enter()
        // .append('g');
      const gw = g.selectAll('.rr').selectAll('text').data(this.data)



        // 绘制矩形 + 过渡效果
        let rectP = 40; // 柱状图间距
        let gt = gs.enter().append('g').attr('class', 'rr')
        let gp = gw.enter()



        gt.
        append('rect')
          .attr('x', function(d,i){
            return scaleX(i) + rectP/2;
          })
          .attr('y',function(d,i){
            // var min = scaleY.domain()[0]; // [0, 73]
            // return scaleY(min);
            scaleY(0)
            // y轴比例尺映射出来的是最大值；这个效果等同于 return height - 2*margin 的效果
          })
          .attr('width',function(d,i){
            return scaleX.step() - rectP;
          })
          .attr('height',function(d,i){
            return 0; // 动画初始状态为0
          })
          .attr('fill','pink')
          .transition('enter-transition')
          .duration(500)
          .delay(function(d,i){
            return i*200 // 每个柱子逐渐开始的效果
          })
          .attr('y',function(d,i){
            return scaleY(d)
          })
          .attr('height',function(d,i){
            return height - margin * 2 - scaleY(d)
          })
        // 添加鼠标划入划出事件
        gs.on("mouseout",function () {
          d3.select(this)
            .transition()
            .duration(200)
            .delay(100)
            .attr('fill','pink');

        })
        gs.on("mouseover",function () {
          d3.select(this) // 这里的this是包含：rect text 的节点
            .transition()
            .duration(200)
            .delay(100)
            .attr('fill','#306ade');
        })

        // 绘文字 + 过渡效果
        // let gb = gs.append('g')
        gp.append('text')
          .attr('x',function(d,i){
            return scaleX(i) + rectP;
          })
          // .attr('y',function(d,i){
          //   return scaleY(this_.data[i]);
          // })
        .text(function(d,i){
          return this_.data2[i];
        }).attr('fill','green')
          .transition()

          .duration(200)
          .delay(function(d,i){
            return i*200;
          })          .attr('y',function(d,i){
          return scaleY(this_.data[i])
        })
          .attr('height',function(d,i){
            return height - margin * 2 - scaleY(d)
          })

        gt.append('text')
          .attr('x',function(d,i){
            return scaleX(i) + rectP;
          })
          // .attr('y',function(d,i){
          //   return scaleY(this_.data[i]);
          // })
          .text(function(d,i){
            return this_.data2[i];
          }).attr('fill','green')
          .transition()

          .duration(200)
          .delay(function(d,i){
            return i*200;
          })          .attr('y',function(d,i){
          return scaleY(this_.data[i])
        })
          .attr('height',function(d,i){
            return height - margin * 2 - scaleY(d)
          })

        //update operation
        gs.transition('update-transition')
          .duration(500)
          .attr('x',function(d,i){
            return scaleX(i) + rectP/2;
          })
          .delay(function(d,i){
            return i*200 // 每个柱子逐渐开始的效果
          })
          .attr('y',function(d,i){
            return scaleY(d)
          })
          .attr('height',function(d,i){
            return height - margin * 2 - scaleY(d)
          })


        gw.transition('update-transition')
          .duration(500)
          .attr('x',function(d,i){
            return scaleX(i) + rectP;
          })
          .text(function(d,i){
            return this_.data2[i]})
          .delay(function(d,i){
            return i*200 // 每个柱子逐渐开始的效果
          })
       .attr('y',function(d,i){
        return scaleY(this_.data[i])
      })
          // .attr('y',function(d,i){
          //   return scaleY(d)
          // })
          // .text(function(d,i){
          //   return this_.data2[i]})

        //delete
        gs.exit().transition('exit-transition')
          .duration(500)
          .attr('height', 0)
          .attr('y', scaleY(0))
          .attr('x', 0)
          .remove()


        // gw.exit().transition('exit-transition')
        //   .duration(500)
        //   .attr('height', 0)
        //   .attr('y', scaleY(0))
        //   .attr('x', 0)
        //   .remove()


      // 删除加上
      //   this.data.shift()
      //   this.data2.shift()
        // gs.data(this.data).exit(
        //   .remove()
        this.data.push(2000)
        this.data.sort((a,b)=>{
          return b-a
        })
        this.data.pop()
        console.log(this.data)
        this.data2.shift()
        this.data2.push('瓦语')
          // .remove()
      },5000)
    },
  },
  created() {
  },
  mounted() {
    this.draw();
  }

};
</script>
<!--<script setup lang="ts">-->
<!--import { ref } from 'vue';-->
<!--import * as d3 from 'd3';-->

<!--</script>-->

<style>
</style>
