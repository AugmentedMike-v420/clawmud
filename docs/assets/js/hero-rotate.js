// Randomly select hero image on page load
document.addEventListener('DOMContentLoaded', function() {
  const heroImages = [
    '/clawmud/assets/images/hero-city.png',
    '/clawmud/assets/images/hero-bike.png',
    '/clawmud/assets/images/hero-cyberspace.png',
    '/clawmud/assets/images/hero-market.png'
  ];
  
  const heroImg = document.querySelector('.hero-bg img');
  if (heroImg) {
    const randomIndex = Math.floor(Math.random() * heroImages.length);
    heroImg.src = heroImages[randomIndex];
  }
});
