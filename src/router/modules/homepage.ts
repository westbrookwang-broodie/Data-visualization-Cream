import { DashboardIcon } from 'tdesign-icons-vue-next';
import { shallowRef } from 'vue';
import Layout from '@/layouts/index.vue';
import index from '@/pages/my-page/index.vue';

export default [
  // {
  //   path: '/dashboard',
  //   component: Layout,
  //   redirect: '/dashboard/base',
  //   name: 'dashboard',
  //   meta: {
  //     title: '仪表盘',
  //     icon: shallowRef(DashboardIcon),
  //     orderNo: 0,
  //   },
  //   children: [
  //     {
  //       path: 'base',
  //       name: 'DashboardBase',
  //       component: () => import('@/pages/dashboard/base/index.vue'),
  //       meta: {
  //         title: '概览仪表盘',
  //       },
  //     },
  //     {
  //       path: 'detail',
  //       name: 'DashboardDetail',
  //       component: () => import('@/pages/dashboard/detail/index.vue'),
  //       meta: {
  //         title: '统计报表',
  //       },
  //     },
  //     {
  //       path: 'detail',
  //       name: 'DashboardDetail',
  //       component: () => import('@/pages/dashboard/detail/index.vue'),
  //       meta: {
  //         title: '统计报表',
  //       },
  //     },
  //     {
  //       path: "new-page",
  //       name: 'index',
  //       title: "新页面侧边栏标题",
  //       component: ()=> import('@/pages/my-page/index.vue'),
  //       meta: {
  //         title: '我的页面',
  //       }
  //     },
  //   ],
  // },
  {
    path: "/page",
    name: 'index',
    title: "page",
    component: index,
    meta: {
      title: '我的页面',
    }
  },

];
