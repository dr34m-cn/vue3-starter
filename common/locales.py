"""
@Author：dr34m
@Date  ：2024/8/16 13:52
"""
import locale
import os

import yaml

# 所有语言列表
allLang = {}
# 系统语言
sysLang = None
# 兜底语言
defaultLang = 'zh_CN'


def getSysLang():
    """
    尝试获取系统默认语言
    :return:
    """
    lang = locale.getlocale()[0] or os.environ.get('LANG') or os.environ.get('LC_ALL') or os.environ.get('LC_MESSAGES')
    if lang:
        lang = lang.split(',')[0]
        mapping = {
            'Chinese (Simplified)_China': 'zh_CN',
            'English_United States': 'en_US'
        }
        return mapping.get(lang, lang)
    return defaultLang


def initLang():
    global allLang
    allLang = {}
    if not os.path.exists('locales'):
        raise Exception("No lang path")
    files = os.listdir('locales')
    for file in files:
        if file.endswith('.yaml'):
            filename = os.path.join('locales', file)
            langKey = file[:-5]
            with open(filename, 'r', encoding='utf-8') as f:
                allLang[langKey] = yaml.safe_load(f)
    global sysLang
    sysLang = getOrSetDefaultLang(getSysLang())


def getOrSetDefaultLang(lang):
    """
    获取或设置默认
    :return:
    """
    if lang not in allLang:
        lang = lang.split('_')[0]
        if lang not in allLang:
            lang = defaultLang
    return lang


def t(params, lang=None):
    """
    根据语言获取文字
    :param params: 文字关键字
    :param lang: 所用语言
    :return:
    """
    if lang is None:
        lang = sysLang
    else:
        lang = getOrSetDefaultLang(lang)
    cu = allLang[lang]
    cuDefault = allLang[defaultLang]
    params = params.split('.')
    for item in params:
        cuDefault = cuDefault[item]
        cu = cu[item] if item in cu else cuDefault
    return cu

# # --- 中文 ---
# 'Chinese (Simplified)_China': 'zh_CN',
# 'Chinese (Simplified)_Singapore': 'zh_SG',
# 'Chinese (Traditional)_Taiwan': 'zh_TW',
# 'Chinese (Traditional)_Hong Kong SAR': 'zh_HK',
# 'Chinese (Traditional)_Macao SAR': 'zh_MO',
#
# # --- 英语 ---
# 'English_United States': 'en_US',
# 'English_United Kingdom': 'en_GB',
# 'English_Australia': 'en_AU',
# 'English_Canada': 'en_CA',
# 'English_India': 'en_IN',
# 'English_South Africa': 'en_ZA',
# 'English_New Zealand': 'en_NZ',
# 'English_Ireland': 'en_IE',
#
# # --- 日语 ---
# 'Japanese_Japan': 'ja_JP',
#
# # --- 韩语 ---
# 'Korean_Korea': 'ko_KR',
#
# # --- 法语 ---
# 'French_France': 'fr_FR',
# 'French_Canada': 'fr_CA',
# 'French_Belgium': 'fr_BE',
# 'French_Switzerland': 'fr_CH',
#
# # --- 德语 ---
# 'German_Germany': 'de_DE',
# 'German_Austria': 'de_AT',
# 'German_Switzerland': 'de_CH',
#
# # --- 西班牙语 ---
# 'Spanish_Spain': 'es_ES',
# 'Spanish_Mexico': 'es_MX',
# 'Spanish_Argentina': 'es_AR',
# 'Spanish_Colombia': 'es_CO',
# 'Spanish_Chile': 'es_CL',
# 'Spanish_Peru': 'es_PE',
#
# # --- 葡萄牙语 ---
# 'Portuguese_Portugal': 'pt_PT',
# 'Portuguese_Brazil': 'pt_BR',
#
# # --- 俄语 ---
# 'Russian_Russia': 'ru_RU',
#
# # --- 意大利语 ---
# 'Italian_Italy': 'it_IT',
# 'Italian_Switzerland': 'it_CH',
#
# # --- 荷兰语 ---
# 'Dutch_Netherlands': 'nl_NL',
# 'Dutch_Belgium': 'nl_BE',
#
# # --- 瑞典语 ---
# 'Swedish_Sweden': 'sv_SE',
#
# # --- 丹麦语 ---
# 'Danish_Denmark': 'da_DK',
#
# # --- 挪威语 ---
# 'Norwegian_Norway': 'no_NO',
#
# # --- 芬兰语 ---
# 'Finnish_Finland': 'fi_FI',
#
# # --- 捷克语 ---
# 'Czech_Czechia': 'cs_CZ',
#
# # --- 波兰语 ---
# 'Polish_Poland': 'pl_PL',
#
# # --- 匈牙利语 ---
# 'Hungarian_Hungary': 'hu_HU',
#
# # --- 土耳其语 ---
# 'Turkish_Turkey': 'tr_TR',
#
# # --- 泰语 ---
# 'Thai_Thailand': 'th_TH',
#
# # --- 越南语 ---
# 'Vietnamese_Viet Nam': 'vi_VN',
#
# # --- 印度尼西亚语 ---
# 'Indonesian_Indonesia': 'id_ID',
#
# # --- 马来语 ---
# 'Malay_Malaysia': 'ms_MY',
#
# # --- 希腊语 ---
# 'Greek_Greece': 'el_GR',
#
# # --- 阿拉伯语 ---
# 'Arabic_Saudi Arabia': 'ar_SA',
# 'Arabic_Egypt': 'ar_EG',
# 'Arabic_United Arab Emirates': 'ar_AE',
# 'Arabic_Morocco': 'ar_MA',
#
# # --- 希伯来语 ---
# 'Hebrew_Israel': 'he_IL',
#
# # --- 乌克兰语 ---
# 'Ukrainian_Ukraine': 'uk_UA',
#
# # --- 罗马尼亚语 ---
# 'Romanian_Romania': 'ro_RO',
#
# # --- 保加利亚语 ---
# 'Bulgarian_Bulgaria': 'bg_BG',
#
# # --- 克罗地亚语 ---
# 'Croatian_Croatia': 'hr_HR',
#
# # --- 斯洛伐克语 ---
# 'Slovak_Slovakia': 'sk_SK',
#
# # --- 斯洛文尼亚语 ---
# 'Slovenian_Slovenia': 'sl_SI',
#
# # --- 塞尔维亚语 ---
# 'Serbian_Serbia': 'sr_RS',
#
# # --- 立陶宛语 ---
# 'Lithuanian_Lithuania': 'lt_LT',
#
# # --- 拉脱维亚语 ---
# 'Latvian_Latvia': 'lv_LV',
#
# # --- 爱沙尼亚语 ---
# 'Estonian_Estonia': 'et_EE'
