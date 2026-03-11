# 🕸️ The FineWeb Dataset

Our primary dataset for the JoeyLLM project is the **FineWeb** corpus. 

## 📁 What is FineWeb?

The [FineWeb dataset](https://huggingface.co/datasets/HuggingFaceFW/fineweb), created by Hugging Face, is a massive, cutting-edge resource designed for training Large Language Models (LLMs). It features over 15 trillion tokens of cleaned and deduplicated English web data sourced from CommonCrawl.

Our environment contains the entire **60 TB** dataset, partitioned into thousands of highly compressed **2 GB Parquet files**.



### 📺 Recommended Resource
If you want a quick visual overview of the dataset's release and its significance in the AI space, check out this short summary of how it fits into modern model training: **[Top AI Trends: Hugging Face FineWeb Dataset](https://www.youtube.com/watch?v=1cB5t4H2_Jo)**.

---

## 🏎️ Why We Host It Locally

You will find the complete 60 TB dataset mounted directly in your environment. We house this locally on our high-speed storage network to massively accelerate your data processing capabilities. 

If we did not host this locally, data cleaning would be practically impossible:
* **Massive Download Times:** It would take several days *just* to pull the data from the internet to our servers.
* **Prohibitive Costs:** Repeatedly downloading 60 TB of data across the team would cost a fortune in network egress fees.
* **Wasted Compute:** Processing and cleaning the data over an active internet connection would take weeks, leaving our compute nodes sitting idle while waiting for data to arrive.

---

## ⚡ The Speed of Local Storage

Because the data is hosted locally on our high-performance infrastructure, the system can deliver a 2 GB Parquet file directly to your notebook in **under a second**. 

If you write highly optimized pipeline code, you can process that file in **2 seconds or less**. 

> **💡 Perspective:** > Even at a blistering processing speed of 3 seconds per file, chewing through the entire 60 TB dataset will still take **hours** to complete. This is exactly why you must optimize your code on a subset first! A poorly written pipeline that takes just 30 seconds per file will take *weeks* to finish.
