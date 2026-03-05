# Streamlitアプリ: ADIFファイルをアップロードし、adiftoolsのadifgraph.monthly_band_qso()でグラフを作成・表示・PNGダウンロード
import streamlit as st
import adiftools.adifgraph as adifgraph
import adiftools.adiftools
import io
import os
import tempfile

st.title("ADIF QSO 月別バンド集計グラフ")

uploaded_file = st.file_uploader("ADIFファイルをアップロードしてください", type=["adi", "adif"])


@st.cache_data
def parse_adif(file_bytes: bytes):
	"""ADIFファイルのバイト列を受け取り、DataFrameを返す（結果をキャッシュ）"""
	tmp_path = None
	try:
		with tempfile.NamedTemporaryFile(mode='wb', suffix='.adi', delete=False) as tmp:
			tmp.write(file_bytes)
			tmp_path = tmp.name
		parser = adiftools.adiftools.ADIFParser()
		return parser.read_adi(tmp_path)
	finally:
		if tmp_path is not None:
			os.unlink(tmp_path)


@st.cache_data
def generate_plot_bytes(file_bytes: bytes) -> bytes:
	"""ADIFバイト列からグラフ画像をメモリ上で生成してキャッシュする"""
	adif = parse_adif(file_bytes)
	buf = io.BytesIO()
	adifgraph.monthly_band_qso(adif, buf)
	return buf.getvalue()


if uploaded_file is not None:
	file_bytes = uploaded_file.getvalue()

	img_bytes = generate_plot_bytes(file_bytes)

	# グラフ表示
	st.image(img_bytes, caption="月別バンドQSOグラフ", use_container_width=True)

	# PNGとしてダウンロード
	st.download_button(
		label="グラフをPNGでダウンロード",
		data=img_bytes,
		file_name="monthly_band_qso.png",
		mime="image/png"
	)
