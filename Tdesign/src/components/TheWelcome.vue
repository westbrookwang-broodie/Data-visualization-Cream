<template>
  <div style="padding: 10px">
<!--    <button @click="play('slide_topToBottom')">从顶部滑入、底部滑出</button>-->
<!--    <button @click="play('slide_bottomToTop')">从底部滑入、顶部滑出</button>-->
<!--    <button @click="play('slide_leftToRight')">从左侧滑入、右侧滑出</button>-->
<!--    <button @click="play('slide_rightToLeft')">从右侧滑入、左侧滑出</button>-->
    <div class="view">
      <transition :name="'slide_bottomToTop'">
        <div v-show="active ===1" class="block red" style="padding: -15px" onclick="play('slide_leftToRight')">
          <h1 class="box1" v-show="active ===1">关于电影的数据可视化作品</h1>
          <h2 class="ii" v-show="active ===1" style="margin: -10px">我们分成四类进行讨论:   </h2>
          <a v-show="active ===1" style="padding: -20px">
            <router-link :to="{path: '/moviebox'}">票房趋势图</router-link>
            ,
          </a>
          <br>
          <a v-show="active ===1">
            <router-link :to="{path: '/cloud'}">词云图</router-link>
            ,
          </a>
          <br>
          <a v-show="active ===1">
            <router-link :to="{path: '/part3'}">关于电影具体分析</router-link>
            ,
          </a>
          <br>
          <a v-show="active===1">
            <router-link :to="{path: '/heatMap'}">情感分析</router-link>
            .
          </a>
          <br>
          <span></span>
          <h1 class="box2" v-show="active ===1">来分析数据</h1>
        </div>
      </transition>
      <transition :name="transName">
        <div v-show="active ===2" class="block green" onclick="play('slide_rightToLeft')" style="width: 100%; height: 100%">
          <div class="v-waterfall-content" id="v-waterfall">
            <div v-for="(img, index) in waterfallList" :key="index" class="v-waterfall-item" :style="{top:img.top+'px',left:img.left+'px',width:waterfallImgWidth+'px',height:img.height}">
              <img :src="img.src" alt="">
              <p style="font-size: small;color: #666;margin: 4px;">{{img.title}}</p>
              <p style="font-size: x-small;color: #9e9e9e;margin: 4px;padding-bottom: 6px;">{{img.info}}</p>
            </div>
          </div>

        </div>
      </transition>
    </div>
  </div>
</template>
<script>
// import { createRequire } from 'module';
// const require = createRequire(import.meta.url);
var transName;
transName = ''
var active = 0;

function getImageUrl(name){
  return new URL(name,import.meta.url).href
}

export default {
  data() {
    return {
      transName: '',
      active: 0,
      waterfallList: [],
      imgArr: [
        getImageUrl('../assets/img_7.png'),
        getImageUrl('../assets/img_8.png'),
        getImageUrl('../assets/img_1.png'),
        getImageUrl('../assets/img_2.png'),
        getImageUrl('../assets/img_3.png'),
        getImageUrl('../assets/img_4.png'),
        getImageUrl('../assets/img.png'),
        getImageUrl('../assets/img_5.png'),
        // getImageUrl('.../assets/img_6.png'),
        getImageUrl('../assets/img_9.png'),
        getImageUrl('../assets/img_10.png'),
        getImageUrl('../assets/img_11.png'),
        getImageUrl('../assets/img_12.png'),
        getImageUrl('../assets/img_13.png'),

      ],
      // waterfallImgWidth: 100,
      waterfallImgWidth: 200,// 每个盒子的宽度
      // waterfallImgCol: 5,// 瀑布流的列数
      waterfallImgCol: 5,// 瀑布流的列数
      waterfallImgRight: 8,// 每个盒子的右padding
      waterfallImgBottom: 8,// 每个盒子的下padding
      waterfallDeviationHeight: [],
      imgList: []
    }
  },
  methods: {
    play(name) {
      this.transName = name
      if (this.active === 1) {
        this.active = 2
      } else {
        this.active = 1
      }
      console.log(this.active)
    }
    ,
    calculationWidth() {
      let domWidth = document.getElementById("v-waterfall").offsetWidth;
      if (!this.waterfallImgWidth && this.waterfallImgCol) {
        this.waterfallImgWidth = (domWidth - this.waterfallImgRight * this.waterfallImgCol) / this.waterfallImgCol;
      } else if (this.waterfallImgWidth && !this.waterfallImgCol) {
        this.waterfallImgCol = Math.floor(domWidth / (this.waterfallImgWidth + this.waterfallImgRight))
      }
      //初始化偏移高度数组
      this.waterfallDeviationHeight = new Array(this.waterfallImgCol);
      for (let i = 0; i < this.waterfallDeviationHeight.length; i++) {
        this.waterfallDeviationHeight[i] = 0;
      }
      this.imgPreloading()
    },
    //图片预加载
    imgPreloading() {
      for (let i = 0; i < this.imgList.length; i++) {
        let aImg = new Image();
        aImg.src = this.imgList[i];
        aImg.onload = aImg.onerror = (e) => {
          let imgData = {};
          imgData.height = this.waterfallImgWidth / aImg.width * aImg.height;
          imgData.src = this.imgList[i];
          // imgData.title = '标题';// 说明文字（也可以自己写数组，或者封装json数据，都可以，但是前提是你会相关操作，这里不赘述）
          // imgData.info = '详情说明：啦啦啦啦啦';// 说明文字
          this.waterfallList.push(imgData);
          this.rankImg(imgData);
        }
      }
    },
    //瀑布流布局
    rankImg(imgData) {
      let {
        waterfallImgWidth,
        waterfallImgRight,
        waterfallImgBottom,
        waterfallDeviationHeight,
        waterfallImgCol
      } = this;
      let minIndex = this.filterMin();
      imgData.top = waterfallDeviationHeight[minIndex];
      imgData.left = minIndex * (waterfallImgRight + waterfallImgWidth);
      // waterfallDeviationHeight[minIndex] += imgData.height + waterfallImgBottom;// 不加文字的盒子高度
      waterfallDeviationHeight[minIndex] += imgData.height + waterfallImgBottom + 56;// 加了文字的盒子高度，留出文字的地方（这里设置56px）
      console.log(imgData);
    },
    /**
     * 找到最短的列并返回下标
     * @returns {number} 下标
     */
    filterMin() {
      const min = Math.min.apply(null, this.waterfallDeviationHeight);
      return this.waterfallDeviationHeight.indexOf(min);
    }
  },

  created() {
    var this_ = this
    window.play= function (item) {
      this_.transName = item
      if (this_.active === 1) {
        this_.active = 2
      } else {
        this_.active = 1
      }

    }
    for (let i = 0; i < this.imgArr.length; i++) {
      // this.imgList.push(this.imgArr[Math.round(Math.random() * 8)]);// 图片随机显示
      this.imgList.push(this.imgArr[i]);
    }
  },
  mounted() {
    setTimeout(this.play(),0)
    this.calculationWidth();

  }
}
</script>
<style scoped>
.v-waterfall-content {
  /* 主要 */
  width: 150%;height: 1000px;position: relative;
  /* 次要：设置滚动条，要求固定高度 */
  /*overflow-y: auto;*/
}

.v-waterfall-item {
  /* 主要 */
  float: left;position: absolute;
}

.v-waterfall-item img {
  /* 主要 */
  /* width: auto;height: auto; */
  width: 90%;height: auto;
  /* 次要 */
  border-radius: 6px;
}
.view {
  position: relative;
  height: 1960px;
  width: 1024px;
  /*background: gainsboro;*/
  overflow: hidden;
}

.block {
  position: absolute;
  height: 1960px;
  width: 1024px;
  text-align: center;
  /*color: white;*/
  line-height: 100px;
}
/*.box1 {*/
/*}*/
/*.box2 {*/
/*}*/
.fade-enter-active, .fade-leave-active {
  transition: 1s;
}
.fade-enter, .fade-leave-to{
  opacity: 0;
  transform: translateX(-25rem);
}

/*.red {*/
/*  background: #ff0000;*/
/*}*/

/*.green {*/
/*  background: #574fec;*/
/*}*/

/*滑入——从顶部*/
@keyframes slideIn_top {
  0% {
    top: -100%;
  }
  100% {
    top: 0;
  }
}

/*滑入——从底部*/
@keyframes slideIn_bottom {
  0% {
    top: 100%;
  }
  100% {
    top: 0;
  }
}

/*滑入——从左侧*/
@keyframes slideIn_left {
  0% {
    left: -100%;
  }
  100% {
    left: 0;
  }
}

/*滑入——从右侧*/
@keyframes slideIn_right {
  0% {
    left: 100%;
  }
  100% {
    left: 0;
  }
}

/*滑出——从顶部*/
@keyframes slideOut_top {
  0% {
    top: 0;
  }
  100% {
    top: -100%
  }
}

/*滑出——从底部*/
@keyframes slideOut_bottom {
  0% {
    top: 0;
  }
  100% {
    top: 100%
  }
}

/*滑出——从左侧*/
@keyframes slideOut_left {
  0% {
    left: 0;
  }
  100% {
    left: -100%
  }
}

/*滑出——从右侧*/
@keyframes slideOut_right {
  0% {
    left: 0;
  }
  100% {
    left: 100%
  }
}

/*滑动(滑入)——从顶部滑入,从底部滑出*/
.slide_topToBottom-enter-active {
  animation: slideIn_top 1s;
}

/*滑动(滑出)——从顶部滑入,从底部滑出*/
.slide_topToBottom-leave-active {
  animation: slideOut_bottom 1s;
}

/*滑动(滑入)——从底部滑入,从顶部滑出*/
.slide_bottomToTop-enter-active {
  animation: slideIn_bottom 1s;
}

/*滑动(滑出)——从底部滑入,从顶部滑出*/
.slide_bottomToTop-leave-active {
  animation: slideOut_top 1s;
}

/*滑动(滑入)——从左侧滑入,从右侧滑出*/
.slide_leftToRight-enter-active {
  animation: slideIn_left 1s;
}

/*滑动(滑出)——从左侧滑入,从右侧滑出*/
.slide_leftToRight-leave-active {
  animation: slideOut_right 1s;
}

/*滑动(滑入)——从右侧滑入,从左侧滑出*/
.slide_rightToLeft-enter-active {
  animation: slideIn_right 1s;
}

/*滑动(滑出)——从右侧滑入,从左侧滑出*/
.slide_rightToLeft-leave-active {
  animation: slideOut_left 1s;
}
</style>
