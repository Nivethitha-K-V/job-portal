document.addEventListener('DOMContentLoaded', function () {
  // Auto-dismiss alerts after 4 seconds
  document.querySelectorAll('.alert').forEach(function (alert) {
    setTimeout(function () {
      alert.classList.remove('show');
      alert.classList.add('fade');
    }, 4000);
  });

  // Highlight active sidebar link based on current path
  var path = window.location.pathname;
  document.querySelectorAll('.sidebar .nav-link').forEach(function (link) {
    if (link.getAttribute('href') === path) {
      link.classList.add('active');
    }
  });
});
