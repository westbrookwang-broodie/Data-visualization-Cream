import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import index from '../views/Moviebox.vue'
import Part3View from '@/views/AnalyzingView.vue'
import Part32View from '@/views/AnalyzingKind.vue'
import Part31View from '@/views/AnalyzingYear.vue'
import Part33View from '@/views/AnalyzingDirector.vue'
import Cloud from '@/views/WordCloud.vue'
import Part34View from '@/views/AnalyzingActor.vue'
import HeatMap from "@/views/HeatMap.vue";
import HomePage from '@/views/HomePage.vue'
import RayView from "@/views/RayView.vue";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/relation',
      name: 'relation',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/RelationChart.vue')
    },
    {
      path:'/moviebox',
      name:'moviebox',
      component: index
    },
    {
      path:'/cloud',
      name:'cloud',
      component:Cloud
    },
    {
      path:'/heatMap',
      name:'heatmap',
      component:HeatMap
    },
    {
      path:'/ray',
      name:'RayView',
      component:RayView
    },
    {
      path:'/part3',
      name:'part3',
      component: Part3View
    },
    {
      path:'/part31',
      name:'part31',
      component:Part31View
    },
    {
      path:'/part32',
      name:'part32',
      component:Part32View
    },
    {
      path:'/part33',
      name:'part33',
      component:Part33View
    },
    {
      path:'/part34',
      name:'part34',
      component:Part34View
    }
  ]
})

export default router
