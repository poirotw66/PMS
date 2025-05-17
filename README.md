# 物業管理系統

本專案為一個物業管理系統，旨在協助使用者高效管理名下或代管的各類物業。

## 技術棧

- **後端:** Python + FastAPI (部署於 Cloud Run)
- **前端:** Vue.js + Vite (部署於 Cloud Storage + CDN)
- **資料庫:** Cloud SQL for PostgreSQL (GCP)

## 專案結構

```
PMS/
├── backend/            # 後端應用程式 (Python + FastAPI)
│   ├── app/            # 主要應用程式邏輯
│   ├── Dockerfile      # Docker 配置文件
│   └── requirements.txt # Python 依賴列表
├── frontend/           # 前端應用程式 (Vue.js + Vite)
│   ├── public/         # 公共靜態資源
│   ├── src/            # 前端原始碼
│   │   ├── assets/     # 靜態資源 (圖片、字體等)
│   │   ├── components/ # Vue 組件
│   │   ├── views/      # Vue 視圖
│   │   ├── App.vue     # 根 Vue 組件
│   │   └── main.js     # JavaScript 入口文件
│   ├── index.html      # HTML 入口文件
│   ├── package.json    # Node.js 依賴與腳本
│   └── vite.config.js  # Vite 配置文件
└── README.md           # 專案說明文件
```

## 部署流程

詳細部署流程請參考 [prompt.md](prompt.md) 文件中的說明。