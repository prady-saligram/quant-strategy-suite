<p align="center">
  <img src="docs/logo.svg" alt="Quant Strategy Suite" width="200"/>
</p>

# Quant Strategy Suite

> **“Trade like a quant, build like an engineer.”**

Your all-in-one Python toolkit for designing, backtesting, and deploying algorithmic trading strategies with rock-solid confidence.

<p align="center">
  <a href="#"><img src="https://img.shields.io/badge/python-3.8%2B-blue.svg" alt="Python 3.8+"/></a>
  <a href="#"><img src="https://img.shields.io/badge-build-passing-brightgreen.svg" alt="Build Status"/></a>
  <a href="#"><img src="https://img.shields.io/badge/license-MIT-yellow.svg" alt="License"/></a>
</p>

---

## 🚀 Table of Contents

1. [✨ Features](#-features)
2. [⚙️ Installation](#️-installation)
3. [🎬 Quick Start](#-quick-start)
4. [🛠 Configuration](#-configuration)
5. [📈 Examples](#-examples)
6. [🧩 Architecture](#-architecture)
7. [👩‍💻 Development](#-development)
8. [📄 License](#-license)

---

## ✨ Features

* **Modular Strategy Factory**
  Build, register, and swap out your own entry/exit logic in seconds.

* **High-Speed Backtesting**
  Vectorized data pipelines & caching make backtests run at near-C speeds.

* **Live Trading Connectors**
  Out-of-the-box adapters for Binance, Alpaca, Interactive Brokers, and REST endpoints.

* **Feature Engineering Toolkit**
  Built-in support for rolling stats, TA-lib indicators, custom Python UDFs, and pipeline caching.

* **Flexible Timeframes**
  From tick-by-tick to daily bars: your choice of 1s, 1m, 5m, 1h, 1d.

* **Extensive Reporting & Visualization**
  Auto-generate HTML/PDF performance reports, equity curves, drawdown analyses, and heatmaps.

* **Plugin-Friendly Design**
  Drop in new data sources, metrics, or execution engines via a simple plugin API.

---

## ⚙️ Installation

1. Clone the repo:

   ```bash
   git clone https://github.com/prady-saligram/quant-strategy-suite.git
   cd quant-strategy-suite
   ```

2. Create a virtual environment & install:

   ```bash
   python3 -m venv venv
   source venv/bin/activate       # macOS/Linux
   .\venv\Scripts\Activate.ps1    # Windows PowerShell
   pip install -r requirements.txt
   ```

3. (Optional) Install extras for live trading or plotting:

   ```bash
   pip install "quant-strategy-suite[live]" "quant-strategy-suite[plot]"
   ```

---

## 🎬 Quick Start

1. **Prepare data**

   ```bash
   python -m qss.data.download --symbol BTCUSDT --start 2020-01-01 --end 2025-01-01
   ```

2. **Define your strategy**

   ```python
   # src/strategies/simple_momentum.py
   from qss import Strategy, indicators

   class SimpleMomentum(Strategy):
       def on_new_bar(self, bar):
           mom = indicators.momentum(bar.close, window=15)
           if mom > 0.02:
               self.buy(bar.close)
           elif mom < -0.02:
               self.sell(bar.close)
   ```

3. **Run a backtest**

   ```bash
   python -m qss.backtest \
       --strategy src/strategies/simple_momentum.py \
       --data data/BTCUSDT_1h.csv \
       --cash 10000 \
       --output reports/momentum-report.html
   ```

4. **Go live**

   ```bash
   python -m qss.live \
       --config config/live.yml \
       --strategy src/strategies/simple_momentum.py
   ```

---

## 🛠 Configuration

All settings live in a YAML file:

```yaml
# config/live.yml
exchange: binance
symbol: BTCUSDT
timeframe: 1h
initial_cash: 50000
risk:
  max_drawdown: 0.10
  position_size_pct: 0.05
notifications:
  telegram:
    token: your_bot_token
    chat_id: 12345678
logging:
  level: INFO
  file: logs/live.log
```

---

## 📈 Examples

* **Multi-symbol backtest**

  ```bash
  python -m qss.backtest \
      --patterns "ETHUSDT,BTCUSDT,BNBUSDT" \
      --strategy src/strategies/grid.py \
      --output reports/grid-multiple.html
  ```

* **Parameter sweep**

  ```bash
  python -m qss.optimize \
      --strategy src/strategies/mean_reversion.py \
      --param window 5 10 20 50 \
      --metric sharpe \
      --output reports/sweep-meanrev.csv
  ```

* **Live dry-run**

  ```bash
  python -m qss.live \
      --config config/dryrun.yml \
      --strategy src/strategies/simple_momentum.py \
      --dry-run
  ```

---

## 🧩 Architecture

```text
quant-strategy-suite/
├── src/
│   ├── qss/
│   │   ├── data/           # data ingestion & normalization
│   │   ├── indicators/     # built-in feature generators
│   │   ├── backtest/       # backtesting engine & result collector
│   │   ├── live/           # live trading & execution adapters
│   │   └── utils/          # logging, config, report generation
│   └── strategies/         # user-defined trading strategies
├── tests/                  # pytest suites & fixtures
├── docs/                   # architecture diagrams & user guide
└── scripts/                # handy CLI wrappers
```

---

## 👩‍💻 Development

1. Create a feature branch:

   ```bash
   git checkout -b feature/awesome-indicator
   ```
2. Code, test, lint:

   ```bash
   pytest --maxfail=1 --disable-warnings -q
   flake8 src/
   ```
3. Open a PR, tag reviewers, merge when green.

Please keep commits atomic, tests green, and PR descriptions clear!

---

## 📄 License

Distributed under the [MIT License](LICENSE). See `LICENSE` for details.

---

> Built with ♥ by Prady Saligram
> *Because spreadsheets are for mortals – real quants automate it all.*

> Last touched: 2025-07-11 01:30 UTC
