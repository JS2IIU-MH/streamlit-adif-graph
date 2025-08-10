# Streamlitアプリ: ADIFファイルをアップロードし、adiftoolsのadifgraph.monthly_band_qso()でグラフを作成・表示・PNGダウンロード
import streamlit as st
import adiftools.adifgraph as adifgraph
import adiftools.adiftools
import matplotlib.pyplot as plt
import io

st.title("ADIF QSO 月別バンド集計グラフ")

uploaded_file = st.file_uploader("ADIFファイルをアップロードしてください", type=["adi", "adif"])


if uploaded_file is not None:
	# アップロードファイルの内容をバイト列で取得
	adi_bytes = uploaded_file.read()
	# バイト列をテキストとしてデコード
	adi_text = adi_bytes.decode("utf-8")
	# ADIFファイルを文字列から読み込む
	parser = adiftools.adiftools.ADIFParser()
	import io
	adif = parser.read_adi(io.StringIO(adi_text))

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
