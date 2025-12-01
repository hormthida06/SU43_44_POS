//Contact_Us
document.getElementById('contactForm').addEventListener('submit', function(e) {
    e.preventDefault();
    
    const name = document.getElementById('name').value;
    const email = document.getElementById('email').value;
    const subject = document.getElementById('subject').value;
    const message = document.getElementById('message').value;

    alert(`Thank you, ${name}! Your message about "${subject}" has been sent. We'll reply to ${email} soon.`);
    this.reset();
  });

  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
      e.preventDefault();
      document.querySelector(this.getAttribute('href')).scrollIntoView({
        behavior: 'smooth'
      });
    });
  });


// about_us

const counters = document.querySelectorAll('.stats-counter');
  const speed = 200;

  const animateCounters = () => {
    counters.forEach(counter => {
      const updateCount = () => {
        const target = +counter.getAttribute('data-target');
        const count = +counter.innerText;
        const increment = target / speed;

        if (count < target) {
          counter.innerText = Math.ceil(count + increment);
          setTimeout(updateCount, 20);
        } else {
          counter.innerText = target.toLocaleString();
        }
      };
      updateCount();
    });
  };

  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        animateCounters();
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.5 });

  document.querySelector('.bg-primary').parentElement && observer.observe(document.querySelector('.bg-primary').parentElement);

//Academic

  const statsSection = document.querySelector('.stats-section');
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        document.querySelectorAll('.stat-number').forEach(stat => {
          const targetText = stat.textContent;
          const isPercent = targetText.includes('%');
          const isRatio = targetText.includes(':');
          const target = parseFloat(targetText.replace(/[%:]/g, ''));
          let count = 0;
          const increment = target / 50;
          const timer = setInterval(() => {
            count += increment;
            if (count >= target) {
              stat.textContent = isPercent ? target + '%' : (isRatio ? '1:' + Math.round(target) : target);
              clearInterval(timer);
            } else {
              const display = Math.ceil(count);
              stat.textContent = isPercent ? display + '%' : (isRatio ? '1:' + display : display);
            }
          }, 30);
        });
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.5 });

  observer.observe(statsSection);

//Internship

  document.getElementById('internshipForm').addEventListener('submit', function(e) {
    e.preventDefault();

    const name = document.getElementById('fullName').value;
    const program = document.getElementById('program').value;

    alert(`Thank you, ${name}! Your application for ${program} has been submitted. We'll contact you within 3 business days.`);

    this.reset();
  });

  const statsSection = document.querySelector('.stats-section');
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        document.querySelectorAll('.stat-number').forEach(stat => {
          const target = stat.textContent.replace('+', '').replace('%', '');
          let count = 0;
          const increment = target / 50;
          const timer = setInterval(() => {
            count += increment;
            if (count >= target) {
              stat.textContent = stat.textContent.includes('%') ? target + '%' : target + '+';
              clearInterval(timer);
            } else {
              stat.textContent = Math.ceil(count) + (stat.textContent.includes('%') ? '%' : '+');
            }
          }, 30);
        });
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.5 });

  observer.observe(statsSection);
