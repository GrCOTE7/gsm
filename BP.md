# NewNRJ.com — MVP Habits & Energy App

## 📘 Mini Specifications — MVP NewNRJ

### .🎯 Mission

Create a simple and efficient mobile application allowing a user to:

* Define a few essential habits,
* Track them daily,
* Visualize their progress,
* Receive immediate positive feedback.

The objective: **validate interest, usage and retention** before investing in advanced features.

### 🧪 Hypotheses to validate

* Users want to track **few habits**, but regularly.
* Immediate positive feedback increases retention.
* Simplicity is an advantage (no overload).
* Multi-language increases international reach.
* The name **NewNRJ** is strong enough for an MVP launch.

### 🧱 MVP Constraints

* Minimalist interface, quick to develop.
* Local storage **Postgres** (or SQLite if needed).
* Multi-language from MVP: EN / ES / FR / DE.
* No gamification, no advanced statistics.
* Clean and scalable architecture (FletX).
* Light branding: just the name **NewNRJ** and a simple palette.
* Publication planned on **Google Play Store**.

### 🎨 MVP Visual Identity (simple and quick)

#### Recommended Font

**Montserrat**, **Poppins**, **Inter**

#### Colors

* Energy green: `#00C853`
* Calm blue: `#2962FF`
* Dark background by default (very dark gray), white text for readability

#### Style

* Minimalist
* Simple icons
* No complex illustrations
* Simple logo (MVP) = Simple NewNRJ text with chosen font

## 🏗️ MVP Architecture (Flet / FletX)

### Recommended Structure (FletX)

```mmarkdown
/controllers      → logic
/views            → screens
/models           → Habit, User (later)
/services         → local storage, notifications
/i18n             → language files (EN/ES/FR/DE)
```

---

## 🛡️ BP — Battle Plan MVP NewNRJ (until Google Play publication)

### .🎯 MVP Objective

Allow a user to:

* [ ] Create **simple habits**
* [ ] Manage one of them with the App
* [ ] **Track them daily**
* [ ] See their **progress**
* [ ] Receive **encouragement / positive feedback**

**Nothing more: MVP!**

No gamification, no badges, no advanced statistics.  
Just the essentials to validate the idea.

---

### Preparation

* [-] BP_version - Set App # 0.0.2 src/ in new structure (Entry point = ./main)
* [ ] App : New version ? Yes : App → Install !
* [ ] Git: Push Main → Auto New Version → Push on Ggle Drive - https://rclone.org
* [ ] 1 Register the habit (H) Sport in Database (migration during development)
* [ ] Home page is the habit, but 1 link to manage the habits
* [ ] 2 Highlight it on all pages (header)
* [ ] 3 The countdown button is functional
* [ ] → Make the sports countdown app work again according to new procedure
* [ ] Add a sound at the beginning and end of the 2 sessions
* [ ] Make tic-tac sound the first and last 7 seconds of each session

### 🧩 The 6 minimum screens of the MVP

#### 1) Home / Onboarding screen

* [ ] Simple logo: **NewNRJ** (text only for MVP)
* [ ] Short sentence: "Build new habits. Boost your energy."
* [ ] Button: **Start**

---

#### 2) Habit creation screen

* [ ] Field: Habit name
* [ ] Field: Frequency (daily / simple weekly)
* [ ] Field: Reminder time (optional)
* [ ] Button: **Add Habit**

---

#### 3) Habit list

* [ ] Display the list of habits
* [ ] **Done** button for each habit
* [ ] Progress bar (optional)

---

#### 4) "Check-in" screen

* [ ] Simple animation: **✓**
* [ ] Positive message: "Great! New energy unlocked."

---

#### 5) Minimal history

* [ ] List of days with **✓** or **✗**
* [ ] No need for graphs for MVP

---

#### 6) Settings

* [ ] Language selector: **EN / ES / FR / DE**
* [ ] Light/dark mode (optional)

---

### 🧠 MVP Features — Technical Side

#### Mandatory

* [ ] Create / delete habits
* [ ] Local storage (SQLite for MVP - Will be Postgres in real production)
* [ ] Daily check-in
* [ ] Multi-language (4 languages)
* [ ] Simple and clean UI

#### Optional (if time available)

* [ ] Local notifications
* [ ] Cloud synchronization (later)
* [ ] User account (later)

---

### Future Extensions (after MVP)

* [ ] FastAPI API
* [ ] Auth
* [ ] Cloud sync
* [ ] Gamification
* [ ] Advanced dashboard

---

## 🔥 Next possible steps (Build Roadmap)

* [ ] Generate complete project tree (FletX)
* [ ] Create the **Habit** model (Python)
* [ ] Create MVP controller
* [ ] Implement the **6 minimalist screens**
* [ ] Set up **i18n** system (EN/ES/FR/DE)
* [ ] Prepare a **3-day development plan**
* [ ] Generate first APK
* [ ] Prepare Store Listing
* [ ] Publish on Google Play

---

## 🚀 Build Pipeline (Android)

### Preparation

* [ ] Install Android Studio
* [ ] Install SDK + build tools
* [ ] Configure Flet/FletX environment for Android
* [ ] Generate first local APK

### Internal Tests

* [ ] Test APK on your own phone
* [ ] Test on 1-2 different Android devices
* [ ] Check languages
* [ ] Check permissions
* [ ] Check data persistence

---

## 🏁 Google Play Store Publication

### 1) Developer Account Creation

* [ ] Create a Google Play Developer account
* [ ] Pay one-time fees
* [ ] Configure legal information

### 2) Store Listing Preparation

* [ ] App name: **NewNRJ**
* [ ] Subtitle: "Build new habits. Boost your energy."
* [ ] Short description
* [ ] Long description
* [ ] 512×512 icon
* [ ] Simple splash screen
* [ ] Screenshots (6 screens)
* [ ] Video (optional)

### 3) APK / AAB Preparation

* [ ] Generate an **AAB** (mandatory format)
* [ ] Sign the application
* [ ] Verify signature
* [ ] Check bundle size

### 4) Deployment

* [ ] Upload AAB to Google Play Console
* [ ] Fill out compliance form (permissions, content)
* [ ] Fill out content rating
* [ ] Set distribution countries
* [ ] Deploy to Closed Testing Track
      (Google Play asks to invite 5-10 testers)

### 5) Publication

* [ ] Fix tester feedback
* [ ] Submit to **Production**
* [ ] Wait for Google validation
* [ ] App published 🎉
