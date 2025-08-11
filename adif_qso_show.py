# Streamlitアプリ: ADIFファイルをアップロードし、adiftoolsのadifgraph.monthly_band_qso()でグラフを作成・表示・PNGダウンロード
import streamlit as st
import adiftools.adifgraph as adifgraph
import adiftools.adiftools
import matplotlib.pyplot as plt
import io

st.title("ADIF QSO 月別バンド集計グラフ")

uploaded_file = st.file_uploader("ADIFファイルをアップロードしてください", type=["adi", "adif"])



if uploaded_file is not None:
	# 一時ファイルとして保存
	with open("temp_upload.adi", "wb") as f:
		f.write(uploaded_file.read())

	# ADIFファイルを読み込む
	parser = adiftools.adiftools.ADIFParser()
	adif = parser.read_adi("temp_upload.adi")

	# グラフ作成（PNGファイルとして保存）
	plot_path = "temp_plot.png"
	adifgraph.monthly_band_qso(adif, plot_path)

	# グラフ表示
	with open(plot_path, "rb") as img_file:
		img_bytes = img_file.read()
	st.image(img_bytes, caption="月別バンドQSOグラフ", use_container_width=True)

	# PNGとしてダウンロード
	st.download_button(
		label="グラフをPNGでダウンロード",
		data=img_bytes,
		file_name="monthly_band_qso.png",
		mime="image/png"
	)
