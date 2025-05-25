<template>
  <footer class="footer">
    <div class="container">
      <div class="footer-content">
        <div class="footer-section">
          <h4 class="footer-title">物業管理系統</h4>
          <p class="footer-description">簡化您的物業管理工作，提高效率與客戶滿意度。</p>
        </div>
        <div class="footer-section">
          <h4 class="footer-title">聯絡我們</h4>
          <p>電話：(02) 2345-6789</p>
          <p>電子郵件：contact@pms.example.com</p>
        </div>
        <div class="footer-section">
          <h4 class="footer-title">快速連結</h4>
          <ul class="footer-links">
            <li><router-link to="/">首頁</router-link></li>
            <li><router-link to="/properties">物件管理</router-link></li>
            <li><router-link to="/residents">住戶管理</router-link></li>
          </ul>
        </div>
      </div>
      <div class="footer-bottom">
        <p>&copy; {{ new Date().getFullYear() }} 物業管理系統 | 版權所有</p>
      </div>
    </div>
  </footer>
</template>

<script setup>
</script>

<style scoped>
.footer {
  background-color: var(--primary-color);
  color: white;
  padding: var(--spacing-lg) 0;
  margin-top: var(--spacing-xl);
}

.footer-content {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: var(--spacing-lg);
  margin-bottom: var(--spacing-lg);
}

.footer-section {
  margin-bottom: var(--spacing-md);
}

.footer-title {
  font-size: 1.2rem;
  margin-bottom: var(--spacing-md);
  color: white;
  font-weight: 600;
}

.footer-description {
  color: rgba(255, 255, 255, 0.8);
  line-height: 1.6;
}

.footer-links {
  list-style: none;
  padding: 0;
}

.footer-links li {
  margin-bottom: var(--spacing-xs);
}

.footer-links a {
  color: rgba(255, 255, 255, 0.8);
  text-decoration: none;
  transition: var(--transition);
}

.footer-links a:hover {
  color: white;
  text-decoration: underline;
}

.footer-bottom {
  padding-top: var(--spacing-md);
  border-top: 1px solid rgba(255, 255, 255, 0.2);
  text-align: center;
  color: rgba(255, 255, 255, 0.7);
  font-size: 0.9rem;
}

.footer p {
  margin-bottom: var(--spacing-xs);
}

@media (max-width: 768px) {
  .footer-content {
    grid-template-columns: 1fr;
  }
}
</style>