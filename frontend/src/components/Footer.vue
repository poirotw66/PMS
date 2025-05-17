<template>
  <footer class="footer">
    <div class="content has-text-centered">
      <p>
        <strong>物業管理系統</strong> by <a href="#">Your Name/Company</a>. &copy; {{ new Date().getFullYear() }}
      </p>
    </div>
  </footer>
</template>

<script setup>
</script>

<style scoped>
.footer {
  background-color: #f8f9fa;
  padding: 2rem 1.5rem;
  border-top: 1px solid #dee2e6;
  margin-top: 2rem;
}

.content p {
  font-size: 0.9rem;
  color: #6c757d;
}

.content a {
  color: #007bff;
  text-decoration: none;
}

.content a:hover {
  text-decoration: underline;
}
</style>