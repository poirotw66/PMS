import { createRouter, createWebHistory } from 'vue-router';
import HomeView from '../views/HomeView.vue'; // Assuming a HomeView will be created
import ResidentsView from '../views/ResidentsView.vue';
import PropertiesView from '../views/PropertiesView.vue';
import PaymentsView from '../views/PaymentsView.vue';
import MaintenanceView from '../views/MaintenanceView.vue';
import AnnouncementsView from '../views/AnnouncementsView.vue';
import PotentialCustomersView from '../views/PotentialCustomersView.vue';

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'Home',
      component: HomeView
    },
    {
      path: '/residents',
      name: 'Residents',
      component: ResidentsView
    },
    {
      path: '/properties',
      name: 'Properties',
      component: PropertiesView
    },
    {
      path: '/payments',
      name: 'Payments',
      component: PaymentsView
    },
    {
      path: '/maintenance',
      name: 'Maintenance',
      component: MaintenanceView
    },
    {
      path: '/announcements',
      name: 'Announcements',
      component: AnnouncementsView
    },
    {
      path: '/potential-customers',
      name: 'potential-customers',
      component: PotentialCustomersView
    }
  ]
})

export default router;