from flask import Flask, render_template_string, request, redirect
import sqlite3

app = Flask(__name__)

# ---------- DATABASE ----------
def init_db():
    con = sqlite3.connect("feedback.db")
    cur = con.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT,
            message TEXT
        )
    """)
    con.commit()
    con.close()

# ---------- BASE TEMPLATE ----------
BASE_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>{{ title }}</title>
    <link rel="stylesheet"
    href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css">

    <style>
        * {
            margin:0;
            padding:0;
            box-sizing:border-box;
        }

        body {
            margin:0;
            font-family:'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background:
                linear-gradient(rgba(255,255,255,0.92), rgba(255,255,255,0.92)),
                url('https://images.unsplash.com/photo-1548013146-72479768bada');
            background-size:cover;
            background-attachment:fixed;
            background-position:center;
        }

        body.home {
            background:
                linear-gradient(rgba(255,152,0,0.05), rgba(61,33,79,0.08)),
                url('https://images.unsplash.com/photo-1609947017136-9daf32a5eb16');
            background-size:cover;
            background-position:center;
            background-attachment:fixed;
        }

        /* HEADER */
        .header {
            background:linear-gradient(135deg,#ff9800 0%,#ff6f00 50%,#e65100 100%);
            color:white;
            padding:20px 40px;
            display:flex;
            justify-content:space-between;
            align-items:center;
            box-shadow:0 8px 20px rgba(0,0,0,0.25);
            position:sticky;
            top:0;
            z-index:1000;
            animation:slideDown 0.5s ease-out;
        }

        @keyframes slideDown {
            from {
                transform:translateY(-100%);
                opacity:0;
            }
            to {
                transform:translateY(0);
                opacity:1;
            }
        }

        .left {
            display:flex;
            align-items:center;
            gap:18px;
            animation:fadeIn 0.8s ease-in;
        }

        @keyframes fadeIn {
            from { opacity:0; }
            to { opacity:1; }
        }

        .left .logo-container {
            width:90px;
            height:90px;
            border-radius:50%;
            border:4px solid white;
            overflow:hidden;
            background:white;
            display:flex;
            align-items:center;
            justify-content:center;
            box-shadow:0 6px 15px rgba(0,0,0,0.3);
            transition:transform 0.3s ease;
        }

        .left .logo-container:hover {
            transform:scale(1.1) rotate(5deg);
        }

        .left .logo-container img {
            width:100%;
            height:100%;
            object-fit:cover;
        }

        .temple-name {
            font-size:26px;
            font-weight:bold;
            text-shadow:2px 2px 4px rgba(0,0,0,0.3);
            letter-spacing:1px;
        }

        .right {
            display:flex;
            align-items:center;
            gap:18px;
        }

        .donate {
            background:linear-gradient(135deg,#3d214f,#5a2d6f);
            padding:12px 24px;
            border-radius:30px;
            font-weight:bold;
            transition:all 0.3s ease;
            box-shadow:0 4px 10px rgba(0,0,0,0.2);
        }

        .donate:hover { 
            background:linear-gradient(135deg,#5a2d6f,#3d214f);
            transform:translateY(-3px);
            box-shadow:0 6px 15px rgba(0,0,0,0.3);
        }

        .donate a {
            color:white;
            text-decoration:none;
        }

        .right i {
            font-size:26px;
            color:white;
            transition:all 0.3s ease;
            cursor:pointer;
        }

        .right i:hover { 
            color:#ffd700;
            transform:scale(1.2) rotate(10deg);
        }

        /* MENU */
        .menu {
            background:linear-gradient(135deg,#3d214f,#5a2d6f,#3d214f);
            text-align:center;
            padding:16px;
            box-shadow:0 6px 12px rgba(0,0,0,0.3);
        }

        .menu a {
            color:white;
            margin:0 25px;
            text-decoration:none;
            font-weight:bold;
            font-size:16px;
            transition:all 0.3s ease;
            padding:8px 16px;
            border-radius:20px;
            display:inline-block;
        }

        .menu a:hover { 
            color:#ff9800;
            background:rgba(255,152,0,0.15);
            transform:translateY(-2px);
        }

        /* CONTENT */
        .content {
            background:rgba(255,255,255,0.97);
            padding:50px 70px;
            min-height:400px;
            border-radius:15px;
            margin:40px;
            box-shadow:0 10px 30px rgba(0,0,0,0.25);
            animation:fadeInUp 0.6s ease-out;
        }

        @keyframes fadeInUp {
            from {
                transform:translateY(30px);
                opacity:0;
            }
            to {
                transform:translateY(0);
                opacity:1;
            }
        }

        body.home .content {
            background:rgba(255,255,255,0.88);
            backdrop-filter:blur(10px);
        }

        h2 { 
            color:#3d214f;
            text-shadow:1px 1px 2px rgba(0,0,0,0.1);
        }

        /* GALLERY */
        .gallery {
            display:grid;
            grid-template-columns:repeat(auto-fit,minmax(260px,1fr));
            gap:25px;
            margin-top:20px;
        }

        .gallery > div {
            transition:all 0.4s ease;
        }

        .gallery img {
            width:100%;
            height:220px;
            object-fit:cover;
            border-radius:12px;
            box-shadow:0 6px 15px rgba(0,0,0,0.25);
            transition:all 0.4s ease;
        }

        .gallery > div:hover {
            transform:translateY(-10px);
        }

        .gallery > div:hover > div {
            transform:translateY(0);
        }

        .gallery img:hover { 
            box-shadow:0 12px 25px rgba(0,0,0,0.35);
        }

        /* CONTACT */
        .contact-box {
            display:grid;
            grid-template-columns:1fr 1fr;
            gap:40px;
            align-items:start;
        }

        .contact-info {
            font-size:16px;
            line-height:1.8;
        }

        .contact-info p {
            margin:18px 0;
            padding:15px;
            background:linear-gradient(135deg,rgba(255,152,0,0.05),rgba(61,33,79,0.05));
            border-radius:10px;
            border-left:4px solid #ff9800;
            transition:all 0.3s ease;
        }

        .contact-info p:hover {
            background:linear-gradient(135deg,rgba(255,152,0,0.1),rgba(61,33,79,0.1));
            transform:translateX(5px);
        }

        .map-container {
            width:100%;
            height:450px;
            border-radius:12px;
            overflow:hidden;
            box-shadow:0 8px 20px rgba(0,0,0,0.25);
            border:3px solid #ff9800;
        }

        .map-container iframe {
            width:100%;
            height:100%;
            border:none;
        }

        @media (max-width:768px) {
            .contact-box {
                grid-template-columns:1fr;
            }
        }

        /* DONATE */
        .donate-box {
            text-align:center;
            background:linear-gradient(145deg,#ffffff,#f5f5f5);
            padding:40px;
            border-radius:20px;
            box-shadow:0 10px 30px rgba(0,0,0,0.25);
            border:3px solid #ff9800;
        }

        .donate-box img {
            width:280px;
            margin:25px 0;
            border:5px solid #3d214f;
            border-radius:15px;
            transition:all 0.4s ease;
            box-shadow:0 8px 20px rgba(0,0,0,0.2);
        }

        .donate-box img:hover { 
            transform:scale(1.08) rotate(2deg);
            box-shadow:0 12px 30px rgba(0,0,0,0.3);
        }

        .donate-box button {
            background:linear-gradient(135deg,#ff9800,#ff6f00);
            color:white;
            padding:14px 30px;
            border:none;
            border-radius:30px;
            cursor:pointer;
            font-weight:bold;
            font-size:16px;
            transition:all 0.3s ease;
            box-shadow:0 6px 15px rgba(255,152,0,0.4);
        }

        .donate-box button:hover { 
            background:linear-gradient(135deg,#ff6f00,#e65100);
            transform:translateY(-3px);
            box-shadow:0 8px 20px rgba(255,152,0,0.5);
        }

        /* FEEDBACK */
        .feedback {
            margin-top:60px;
            background:linear-gradient(135deg,#3d214f,#5a2d6f);
            color:white;
            padding:45px;
            border-radius:15px;
            box-shadow:0 10px 30px rgba(0,0,0,0.3);
        }

        .feedback h3 {
            font-size:26px;
            margin-bottom:20px;
            text-shadow:2px 2px 4px rgba(0,0,0,0.3);
        }

        .feedback input, .feedback textarea {
            width:100%;
            padding:14px;
            margin-bottom:15px;
            border:2px solid rgba(255,255,255,0.3);
            border-radius:8px;
            font-size:15px;
            transition:all 0.3s ease;
            background:rgba(255,255,255,0.95);
        }

        .feedback input:focus, .feedback textarea:focus {
            outline:none;
            border-color:#ff9800;
            box-shadow:0 0 10px rgba(255,152,0,0.3);
            transform:scale(1.02);
        }

        .feedback button {
            background:linear-gradient(135deg,#ff9800,#ff6f00);
            border:none;
            padding:12px 30px;
            font-weight:bold;
            font-size:16px;
            cursor:pointer;
            border-radius:30px;
            transition:all 0.3s ease;
            box-shadow:0 6px 15px rgba(255,152,0,0.4);
        }

        .feedback button:hover { 
            background:linear-gradient(135deg,#ff6f00,#e65100);
            transform:translateY(-2px);
            box-shadow:0 8px 20px rgba(255,152,0,0.5);
        }

        footer {
            background:linear-gradient(135deg,#1a1a1a,#2d2d2d);
            color:white;
            text-align:center;
            padding:20px;
            font-size:15px;
            box-shadow:0 -5px 15px rgba(0,0,0,0.3);
        }
    </style>
</head>

<body class="{{ page_class }}">

<!-- HEADER -->
<div class="header">
    <div class="left">
        <div class="logo-container">
            <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/5/5c/Ganesha_basohli_miniature.jpg/800px-Ganesha_basohli_miniature.jpg" alt="Temple Logo">
        </div>
        <div>
            <div class="temple-name">Sri Ganesha Temple</div>
            <div>Srirangapatna, Karnataka</div>
        </div>
    </div>

    <div class="right">
        <div class="donate"><a href="/donate">DONATE</a></div>
        <a href="https://wa.me/919999999999"><i class="fab fa-whatsapp"></i></a>
        <a href="https://instagram.com"><i class="fab fa-instagram"></i></a>
        <a href="https://facebook.com"><i class="fab fa-facebook"></i></a>
    </div>
</div>

<!-- MENU -->
<div class="menu">
    <a href="/">HOME</a>
    <a href="/about">ABOUT</a>
    <a href="/gallery">GALLERY</a>
    <a href="/contact">CONTACT</a>
</div>

<!-- CONTENT -->
<div class="content">
    {{ content|safe }}
</div>

<!-- FEEDBACK -->
<div class="feedback">
    <h3><i class="fas fa-comments"></i> Devotee Feedback</h3>
    <form method="post">
        <input name="name" placeholder="Your Name" required>
        <input name="email" placeholder="Email" required>
        <textarea name="message" placeholder="Share your experience with us..." rows="4"></textarea>
        <button type="submit"><i class="fas fa-paper-plane"></i> Submit Feedback</button>
    </form>
</div>

<footer>
    © 2026 Sri Ganesha Temple | All Rights Reserved | Built with Devotion 🙏
</footer>

</body>
</html>
"""

# ---------- ROUTES ----------
@app.route("/", methods=["GET","POST"])
def home():
    if request.method == "POST":
        save_feedback()
        return redirect("/")
    content = """
    <h2 style="text-align:center;font-size:36px;margin-bottom:15px;">🙏 Welcome to Sri Ganesha Temple 🙏</h2>
    <p style="font-size:18px;line-height:1.9;text-align:center;max-width:900px;margin:0 auto 40px auto;color:#555;">
    Experience divine peace and blessings in a sacred environment dedicated to Lord Ganesha, 
    the remover of obstacles and the deity of wisdom, prosperity, and new beginnings.
    </p>
    
    <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:30px;margin-top:50px;">
        <div style="background:linear-gradient(135deg,#fff,#fef8f0);padding:30px;border-radius:15px;box-shadow:0 8px 20px rgba(0,0,0,0.15);border-left:5px solid #ff9800;transition:all 0.3s ease;">
            <h3 style="color:#ff9800;margin-top:0;font-size:22px;"><i class="fas fa-om"></i> Daily Poojas</h3>
            <p style="margin:15px 0;"><strong>Morning Pooja:</strong> 6:00 AM - 8:00 AM</p>
            <p style="margin:15px 0;"><strong>Afternoon Pooja:</strong> 12:00 PM - 1:00 PM</p>
            <p style="margin:15px 0;"><strong>Evening Aarti:</strong> 7:00 PM - 8:00 PM</p>
            <p style="color:#666;font-size:14px;margin-top:20px;font-style:italic;">Join us for daily rituals and divine blessings</p>
        </div>
        
        <div style="background:linear-gradient(135deg,#fff,#f5f0fe);padding:30px;border-radius:15px;box-shadow:0 8px 20px rgba(0,0,0,0.15);border-left:5px solid #3d214f;transition:all 0.3s ease;">
            <h3 style="color:#3d214f;margin-top:0;font-size:22px;"><i class="fas fa-calendar-alt"></i> Special Events</h3>
            <p style="margin:15px 0;"><strong>Ganesh Chaturthi</strong> - 10-day celebration</p>
            <p style="margin:15px 0;"><strong>Sankashti Chaturthi</strong> - Monthly pooja</p>
            <p style="margin:15px 0;"><strong>Vinayaka Jayanti</strong> - Annual festival</p>
            <p style="color:#666;font-size:14px;margin-top:20px;font-style:italic;">Celebrate with devotional fervor</p>
        </div>
        
        <div style="background:linear-gradient(135deg,#fff,#fef8f0);padding:30px;border-radius:15px;box-shadow:0 8px 20px rgba(0,0,0,0.15);border-left:5px solid #ff6f00;transition:all 0.3s ease;">
            <h3 style="color:#ff6f00;margin-top:0;font-size:22px;"><i class="fas fa-hands-helping"></i> Services</h3>
            <p style="margin:15px 0;"><strong>Annadanam</strong> - Free daily meals</p>
            <p style="margin:15px 0;"><strong>Archana</strong> - Special offerings</p>
            <p style="margin:15px 0;"><strong>Vedic Classes</strong> - Traditional learning</p>
            <p style="color:#666;font-size:14px;margin-top:20px;font-style:italic;">Participate in community service</p>
        </div>
    </div>
    
    <div style="margin-top:60px;background:linear-gradient(to right,rgba(255,152,0,0.1),rgba(61,33,79,0.1));padding:40px;border-radius:15px;border:3px solid #ff9800;">
        <h3 style="color:#3d214f;text-align:center;font-size:28px;margin-bottom:30px;"><i class="fas fa-star"></i> Why Visit Sri Ganesha Temple?</h3>
        <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:25px;">
            <div style="text-align:center;padding:20px;">
                <i class="fas fa-heart" style="font-size:50px;color:#ff9800;margin-bottom:15px;"></i>
                <h4 style="color:#3d214f;margin:10px 0;">Spiritual Serenity</h4>
                <p style="font-size:14px;color:#666;">Find peace in our sacred premises</p>
            </div>
            <div style="text-align:center;padding:20px;">
                <i class="fas fa-people-carry" style="font-size:50px;color:#ff9800;margin-bottom:15px;"></i>
                <h4 style="color:#3d214f;margin:10px 0;">Community</h4>
                <p style="font-size:14px;color:#666;">Join vibrant devotee gatherings</p>
            </div>
            <div style="text-align:center;padding:20px;">
                <i class="fas fa-book-open" style="font-size:50px;color:#ff9800;margin-bottom:15px;"></i>
                <h4 style="color:#3d214f;margin:10px 0;">Ancient Wisdom</h4>
                <p style="font-size:14px;color:#666;">Learn vedic knowledge</p>
            </div>
            <div style="text-align:center;padding:20px;">
                <i class="fas fa-praying-hands" style="font-size:50px;color:#ff9800;margin-bottom:15px;"></i>
                <h4 style="color:#3d214f;margin:10px 0;">Divine Blessings</h4>
                <p style="font-size:14px;color:#666;">Receive Lord Ganesha's grace</p>
            </div>
        </div>
    </div>
    
    <div style="margin-top:50px;text-align:center;background:linear-gradient(135deg,#3d214f,#5a2d6f);color:white;padding:35px;border-radius:15px;box-shadow:0 8px 20px rgba(0,0,0,0.2);">
        <h3 style="color:#ff9800;font-size:24px;margin-bottom:15px;">💬 Devotee Testimonials</h3>
        <p style="font-style:italic;font-size:17px;margin:20px 0;line-height:1.8;">
        "Visiting this temple changed my life. The peaceful atmosphere and divine energy are truly remarkable."
        </p>
        <p style="font-size:14px;color:#ccc;">- Rajesh Kumar, Bengaluru</p>
    </div>
    """
    return render_template_string(BASE_HTML, title="Home", content=content, page_class="home")

@app.route("/about", methods=["GET","POST"])
def about():
    if request.method == "POST":
        save_feedback()
        return redirect("/about")
    return render_template_string(BASE_HTML, title="About", content="""
        <h2 style="text-align:center;font-size:36px;margin-bottom:40px;">About Sri Ganesha Temple</h2>
        
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:40px;margin-top:30px;">
            <div>
                <img src="https://images.unsplash.com/photo-1609947017136-9daf32a5eb16" 
                     style="width:100%;height:350px;object-fit:cover;border-radius:15px;box-shadow:0 8px 20px rgba(0,0,0,0.25);">
            </div>
            <div>
                <h3 style="color:#ff9800;margin-top:0;font-size:24px;"><i class="fas fa-history"></i> Our Heritage</h3>
                <p style="line-height:1.9;color:#333;font-size:16px;">
                Established over 200 years ago, Sri Ganesha Temple stands as a beacon of spiritual enlightenment 
                in Srirangapatna, Karnataka. The temple follows authentic South Indian Agama traditions and has 
                been a center of devotion for countless generations of devotees.
                </p>
                <p style="line-height:1.9;color:#333;font-size:16px;margin-top:20px;">
                The temple deity, Lord Ganesha, is beautifully carved from a single piece of black stone and 
                radiates divine energy that brings peace and prosperity to all who visit.
                </p>
            </div>
        </div>
        
        <div style="margin-top:60px;">
            <h3 style="color:#3d214f;text-align:center;font-size:26px;margin-bottom:20px;"><i class="fas fa-dharmachakra"></i> Temple Philosophy</h3>
            <p style="text-align:center;font-size:17px;line-height:1.9;max-width:850px;margin:20px auto;color:#555;">
            We believe in preserving ancient traditions while serving the modern devotee. Our temple is a place where 
            spirituality meets community service, where rituals blend with education, and where every visitor finds solace 
            and divine grace.
            </p>
        </div>
        
        <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:30px;margin-top:50px;">
            <div style="background:linear-gradient(135deg,#ff9800,#ff6f00);color:white;padding:35px;border-radius:15px;text-align:center;box-shadow:0 8px 20px rgba(255,152,0,0.3);transition:transform 0.3s ease;">
                <i class="fas fa-temple" style="font-size:55px;margin-bottom:20px;"></i>
                <h4 style="margin:15px 0;font-size:20px;">Architecture</h4>
                <p style="font-size:15px;line-height:1.7;">Traditional Dravidian style with intricate carvings and sanctum sanctorum</p>
            </div>
            
            <div style="background:linear-gradient(135deg,#3d214f,#5a2d6f);color:white;padding:35px;border-radius:15px;text-align:center;box-shadow:0 8px 20px rgba(61,33,79,0.3);transition:transform 0.3s ease;">
                <i class="fas fa-users" style="font-size:55px;margin-bottom:20px;"></i>
                <h4 style="margin:15px 0;font-size:20px;">Community</h4>
                <p style="font-size:15px;line-height:1.7;">Over 5,000 regular devotees from all walks of life</p>
            </div>
            
            <div style="background:linear-gradient(135deg,#ff9800,#ff6f00);color:white;padding:35px;border-radius:15px;text-align:center;box-shadow:0 8px 20px rgba(255,152,0,0.3);transition:transform 0.3s ease;">
                <i class="fas fa-hands" style="font-size:55px;margin-bottom:20px;"></i>
                <h4 style="margin:15px 0;font-size:20px;">Service</h4>
                <p style="font-size:15px;line-height:1.7;">Daily annadanam, medical camps, and educational programs</p>
            </div>
        </div>
        
        <div style="margin-top:60px;background:#f9f9f9;padding:40px;border-radius:15px;border-left:6px solid #ff9800;box-shadow:0 6px 15px rgba(0,0,0,0.1);">
            <h3 style="color:#3d214f;margin-top:0;font-size:24px;"><i class="fas fa-list-ul"></i> Temple Festivals & Celebrations</h3>
            <div style="display:grid;grid-template-columns:1fr 1fr;gap:30px;margin-top:25px;">
                <div>
                    <p style="margin-bottom:20px;"><strong style="color:#ff9800;font-size:18px;">🎉 Ganesh Chaturthi</strong><br>
                    <span style="color:#666;font-size:15px;line-height:1.8;">10-day grand celebration with special poojas, cultural programs, and prasadam distribution</span></p>
                    
                    <p style="margin-top:25px;"><strong style="color:#ff9800;font-size:18px;">🌙 Sankashti Chaturthi</strong><br>
                    <span style="color:#666;font-size:15px;line-height:1.8;">Monthly observance with evening prayers and fasting</span></p>
                </div>
                
                <div>
                    <p style="margin-bottom:20px;"><strong style="color:#ff9800;font-size:18px;">✨ Vinayaka Jayanti</strong><br>
                    <span style="color:#666;font-size:15px;line-height:1.8;">Annual birthday celebration with elaborate rituals</span></p>
                    
                    <p style="margin-top:25px;"><strong style="color:#ff9800;font-size:18px;">🪔 Diwali</strong><br>
                    <span style="color:#666;font-size:15px;line-height:1.8;">Festival of lights with special decorations and offerings</span></p>
                </div>
            </div>
        </div>
        
        <div style="margin-top:50px;background:linear-gradient(to right,rgba(61,33,79,0.08),rgba(255,152,0,0.08));padding:35px;border-radius:12px;text-align:center;">
            <h3 style="color:#3d214f;font-size:24px;"><i class="fas fa-quote-left"></i> Temple Management</h3>
            <p style="line-height:1.9;color:#555;max-width:750px;margin:20px auto;font-size:16px;">
            The temple is managed by a dedicated trust committee comprising respected community members, 
            priests, and devotees who work tirelessly to maintain the sanctity and serve the devotees with utmost devotion.
            All donations are transparently utilized for temple maintenance, rituals, and charitable activities.
            </p>
        </div>
        """, page_class="")

@app.route("/gallery", methods=["GET","POST"])
def gallery():
    if request.method == "POST":
        save_feedback()
        return redirect("/gallery")
    return render_template_string(BASE_HTML, title="Gallery", content="""
        <div style="text-align:center;margin-bottom:50px;">
            <h2 style="color:#3d214f;font-size:38px;margin-bottom:15px;">
                <i class="fas fa-images"></i> Temple Photo Gallery
            </h2>
            <p style="font-size:18px;color:#666;max-width:850px;margin:0 auto;line-height:1.9;">
            Experience the divine beauty and sacred atmosphere of Sri Ganesha Temple through these carefully curated photographs. 
            Each image tells a story of devotion, tradition, and spiritual heritage.
            </p>
        </div>
        
        <div style="background:linear-gradient(135deg,#ff9800 0%,#ff6f00 50%,#e65100 100%);color:white;padding:30px;border-radius:15px;margin-bottom:50px;text-align:center;box-shadow:0 8px 20px rgba(255,152,0,0.3);">
            <h3 style="margin:0 0 10px 0;font-size:24px;"><i class="fas fa-star"></i> Featured Temple Moments</h3>
            <p style="margin:0;font-size:16px;opacity:0.95;">Witness the grandeur of our sacred temple through these authentic photographs</p>
        </div>
        
        <div class="gallery">
            <div style="position:relative;overflow:hidden;border-radius:12px;">
                <img src="https://images.unsplash.com/photo-1588013273468-315fd88ea34c?w=800" alt="Lord Ganesha">
                <div style="position:absolute;bottom:0;left:0;right:0;background:linear-gradient(to top,rgba(0,0,0,0.95),rgba(0,0,0,0.7),transparent);color:white;padding:20px;transform:translateY(100%);transition:transform 0.4s ease;">
                    <h4 style="margin:0 0 8px 0;font-size:18px;color:#ff9800;">Lord Ganesha Deity</h4>
                    <p style="margin:0;font-size:14px;opacity:0.9;">The magnificent idol of Lord Ganesha adorned with fresh flowers and traditional decorations</p>
                </div>
            </div>
            
            <div style="position:relative;overflow:hidden;border-radius:12px;">
                <img src="https://images.unsplash.com/photo-1548013146-72479768bada?w=800" alt="Inner Sanctum">
                <div style="position:absolute;bottom:0;left:0;right:0;background:linear-gradient(to top,rgba(0,0,0,0.95),rgba(0,0,0,0.7),transparent);color:white;padding:20px;">
                    <h4 style="margin:0 0 8px 0;font-size:18px;color:#ff9800;">Sacred Inner Sanctum</h4>
                    <p style="margin:0;font-size:14px;opacity:0.9;">The peaceful prayer hall where devotees connect with the divine</p>
                </div>
            </div>
            
            <div style="position:relative;overflow:hidden;border-radius:12px;">
                <img src="https://images.unsplash.com/photo-1508672019048-805c876b67e2?w=800" alt="Evening Aarti">
                <div style="position:absolute;bottom:0;left:0;right:0;background:linear-gradient(to top,rgba(0,0,0,0.95),rgba(0,0,0,0.7),transparent);color:white;padding:20px;">
                    <h4 style="margin:0 0 8px 0;font-size:18px;color:#ff9800;">Evening Aarti Ceremony</h4>
                    <p style="margin:0;font-size:14px;opacity:0.9;">The mesmerizing evening aarti with traditional oil lamps</p>
                </div>
            </div>
        </div>
        
        <div style="margin-top:70px;background:linear-gradient(135deg,#3d214f,#5a2d6f,#7a4d8f);color:white;padding:50px;border-radius:20px;box-shadow:0 12px 35px rgba(61,33,79,0.4);text-align:center;">
            <i class="fas fa-camera-retro" style="font-size:60px;margin-bottom:20px;color:#ff9800;"></i>
            <h3 style="margin:0 0 20px 0;font-size:28px;">Share Your Divine Moments</h3>
            <p style="font-size:17px;line-height:1.9;max-width:750px;margin:0 auto 30px auto;">
            Have you captured beautiful moments during your visit to Sri Ganesha Temple? We would be honored to feature 
            your photographs in our gallery. Share your spiritual journey and inspire others!
            </p>
            <div style="background:rgba(255,255,255,0.12);padding:25px;border-radius:12px;display:inline-block;margin-top:15px;">
                <p style="margin:0 0 12px 0;font-size:16px;">
                    <i class="fas fa-envelope" style="color:#ff9800;"></i> <strong>Email:</strong> sriganeshatemple@gmail.com
                </p>
                <p style="margin:0;font-size:16px;">
                    <i class="fab fa-instagram" style="color:#ff9800;"></i> <strong>Instagram:</strong> #SriGaneshaTemple
                </p>
            </div>
        </div>
        
        <div style="margin-top:50px;display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:25px;">
            <div style="background:linear-gradient(135deg,rgba(255,152,0,0.1),rgba(255,152,0,0.05));padding:30px;border-radius:15px;text-align:center;border:2px solid rgba(255,152,0,0.3);transition:transform 0.3s ease;">
                <i class="fas fa-images" style="font-size:45px;color:#ff9800;margin-bottom:15px;"></i>
                <h4 style="color:#3d214f;margin:0 0 10px 0;font-size:20px;">2 Featured Photos</h4>
                <p style="color:#666;margin:0;font-size:15px;">Handpicked images showcasing temple beauty</p>
            </div>
            
            <div style="background:linear-gradient(135deg,rgba(61,33,79,0.1),rgba(61,33,79,0.05));padding:30px;border-radius:15px;text-align:center;border:2px solid rgba(61,33,79,0.3);transition:transform 0.3s ease;">
                <i class="fas fa-gopuram" style="font-size:45px;color:#3d214f;margin-bottom:15px;"></i>
                <h4 style="color:#3d214f;margin:0 0 10px 0;font-size:20px;">Authentic Moments</h4>
                <p style="color:#666;margin:0;font-size:15px;">Real photographs from daily temple life</p>
            </div>
            
            <div style="background:linear-gradient(135deg,rgba(255,152,0,0.1),rgba(255,152,0,0.05));padding:30px;border-radius:15px;text-align:center;border:2px solid rgba(255,152,0,0.3);transition:transform 0.3s ease;">
                <i class="fas fa-pray" style="font-size:45px;color:#ff9800;margin-bottom:15px;"></i>
                <h4 style="color:#3d214f;margin:0 0 10px 0;font-size:20px;">Sacred Traditions</h4>
                <p style="color:#666;margin:0;font-size:15px;">Capturing centuries-old rituals</p>
            </div>
        </div>
        
        <div style="margin-top:40px;text-align:center;padding:30px;background:linear-gradient(to right,rgba(255,152,0,0.08),rgba(61,33,79,0.08));border-radius:12px;border:2px dashed #ff9800;">
            <p style="color:#666;font-size:15px;margin:0;line-height:1.9;">
            <i class="fas fa-info-circle" style="color:#ff9800;font-size:18px;"></i> <strong style="color:#3d214f;">Photography Guidelines:</strong> 
            All photographs are taken with utmost respect for temple sanctity. Visitors are requested to seek permission before photography. 
            Flash photography and photography during certain sacred ceremonies may be restricted.
            </p>
        </div>
        """, page_class="")

@app.route("/contact", methods=["GET","POST"])
def contact():
    if request.method == "POST":
        save_feedback()
        return redirect("/contact")
    return render_template_string(BASE_HTML, title="Contact", content="""
        <h2 style="text-align:center;font-size:36px;margin-bottom:40px;">📞 Contact Us</h2>
        <div class="contact-box">
            <div class="contact-info">
                <p><i class="fas fa-map-marker-alt" style="color:#ff9800;font-size:20px;"></i> <strong>Address:</strong><br>
                Sri Ganesha Temple<br>
                Srirangapatna, Karnataka 571438</p>
                
                <p><i class="fas fa-phone" style="color:#ff9800;font-size:20px;"></i> <strong>Phone:</strong><br>
                +91 99999 99999</p>
                
                <p><i class="fas fa-envelope" style="color:#ff9800;font-size:20px;"></i> <strong>Email:</strong><br>
                sriganeshatemple@gmail.com</p>
                
                <p><i class="fas fa-clock" style="color:#ff9800;font-size:20px;"></i> <strong>Temple Timings:</strong><br>
                Morning: 6:00 AM - 12:00 PM<br>
                Evening: 5:00 PM - 9:00 PM</p>
            </div>
            
            <div class="map-container">
                <iframe 
                    src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d62267.76399897147!2d76.6494!3d12.4184!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x3baf70381d572aa9%3A0x2b89ece8c0d05a7c!2sSrirangapatna%2C%20Karnataka!5e0!3m2!1sen!2sin!4v1234567890"
                    allowfullscreen=""
                    loading="lazy"
                    referrerpolicy="no-referrer-when-downgrade">
                </iframe>
            </div>
        </div>
        """, page_class="")

@app.route("/donate")
def donate():
    return render_template_string(BASE_HTML, title="Donate", content="""
        <div class="donate-box">
            <h2 style="color:#3d214f;font-size:32px;margin-bottom:15px;"><i class="fas fa-hands-heart"></i> Support the Temple</h2>
            <p style="font-size:17px;color:#555;line-height:1.8;max-width:600px;margin:0 auto 20px auto;">
            Your generous donation helps temple maintenance, grand festivals, daily annadanam, 
            and various charitable activities that serve the community.
            </p>
            <img src="https://api.qrserver.com/v1/create-qr-code/?size=280x280&data=upi://pay?pa=ganesha@upi&pn=Sri%20Ganesha%20Temple" alt="Donate QR Code">
            <p style="margin:20px 0;font-size:18px;"><strong>UPI ID:</strong> <span style="color:#ff9800;">ganesha@upi</span></p>
            <button><i class="fas fa-qrcode"></i> Scan & Donate</button>
            <div style="margin-top:30px;padding:20px;background:rgba(255,152,0,0.1);border-radius:10px;">
                <p style="margin:0;color:#666;font-size:14px;">
                <i class="fas fa-shield-alt" style="color:#ff9800;"></i> All donations are used transparently for temple activities
                </p>
            </div>
        </div>
        """, page_class="")

# ---------- FEEDBACK SAVE ----------
def save_feedback():
    con = sqlite3.connect("feedback.db")
    cur = con.cursor()
    cur.execute(
        "INSERT INTO feedback(name,email,message) VALUES (?,?,?)",
        (
            request.form.get("name"),
            request.form.get("email"),
            request.form.get("message")
        )
    )
    con.commit()
    con.close()

# ---------- RUN ----------
if __name__ == "__main__":
    init_db()
    app.run(debug=True)
