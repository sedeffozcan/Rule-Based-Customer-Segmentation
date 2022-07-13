
# Soru 1: persona.csv dosyasını okutunuz ve veri seti ile ilgili genel bilgileri gösteriniz
import pandas as pd
data_set=pd.read_csv("/Users/sedeftaskin/Desktop/Data_Science/VBO/Homeworks/WEEK2/Kural_Tabanli_Siniflandirma/persona.csv")
df=data_set.copy()
df.head()

def check_df(dataframe, head=5):
    print("##################### Shape #####################")
    print(dataframe.shape)
    print("##################### Types #####################")
    print(dataframe.dtypes)
    print("##################### Head #####################")
    print(dataframe.head(head))
    print("##################### Tail #####################")
    print(dataframe.tail(head))
    print("##################### NA #####################")
    print(dataframe.isnull().sum())
    print("##################### Quantiles #####################")
    print(dataframe.describe([0, 0.05, 0.50, 0.95, 0.99, 1]).T)

check_df(df)
df.info
df.describe().T

# Soru 2: Kaç unique SOURCE vardır? Frekansları nedir?

df["SOURCE"].nunique()
df["SOURCE"].value_counts()

# Soru 3: Kaç unique PRICE vardır?

df["PRICE"].nunique()

#Soru 4: Hangi PRICE'dan kaçar tane satış gerçekleşmiş?

df["PRICE"].value_counts()

# Soru 5: Hangi ülkeden kaçar tane satış olmuş?

df["COUNTRY"].value_counts()

# Soru 6: Ülkelere göre satışlardan toplam ne kadar kazanılmış?

df.groupby("COUNTRY")["PRICE"].sum()
df.groupby("COUNTRY").agg({"PRICE":"sum"})

# Soru 7: SOURCE türlerine göre satış sayıları nedir?

df["SOURCE"].value_counts()
df.groupby("SOURCE")["PRICE"].count()

# Soru 8: Ülkelere göre PRICE ortalamaları nedir?

df.groupby("COUNTRY")["PRICE"].mean()
df.groupby("COUNTRY").agg({"PRICE":"mean"})

# Soru 9: SOURCE'lara göre PRICE ortalamaları nedir?

df.groupby("SOURCE")["PRICE"].mean()
df.groupby("SOURCE").agg({"PRICE":"mean"})

#  Soru 10: COUNTRY-SOURCE kırılımında PRICE ortalamaları nedir?

df.groupby(["SOURCE","COUNTRY"])["PRICE"].mean()
df.groupby(["SOURCE","COUNTRY"]).agg({"PRICE":"mean"})

# GÖREV 2: COUNTRY, SOURCE, SEX, AGE kırılımında ortalama kazançlar nedir?

df.groupby(["SOURCE","COUNTRY","SEX","AGE"]).agg({"PRICE":"mean"})

# Görev 3: Çıktıyı PRICE’a göre sıralayınız.
#  Önceki sorudaki çıktıyı daha iyi görebilmek için sort_values metodunu azalan olacak şekilde PRICE’a göre uygulayınız.
# Çıktıyı agg_df olarak kaydediniz.

agg_df=df.groupby(["SOURCE","COUNTRY","SEX","AGE"]).agg({"PRICE":"mean"}).sort_values("PRICE",ascending=False)
agg_df

# Görev 4: Görev 4: Indekste yer alan isimleri değişken ismine çeviriniz.
# Üçüncü sorunun çıktısında yer alan PRICE dışındaki tüm değişkenler index isimleridir. Bu isimleri değişken isimlerine çeviriniz.

agg_df.reset_index(inplace=True)
agg_df

# Görev 5: Age değişkenini kategorik değişkene çeviriniz ve agg_df’e ekleyiniz.
# Age sayısal değişkenini kategorik değişkene çeviriniz.
# Aralıkları ikna edici şekilde oluşturunuz.
# Örneğin: ‘0_18', ‘19_23', '24_30', '31_40', '41_70'
# first way

agg_df['AGE_CAT'] = pd.cut(x=agg_df['AGE'],
                           bins=[0, 18, 23, 30, 40, 70],
                           labels=['0_18', '19_23', '24_30', '31_40', '41_70'])
# second way

agg_df["AGE_CAT"]=pd.cut(df["AGE"],[0,18,23,30,40,70],labels=['0_18', '19_23', '24_30', '31_40', '41_70'])
agg_df

# Görev 6: Yeni seviye tabanlı müşterileri (persona) tanımlayınız.
# Yeni seviye tabanlı müşterileri (persona) tanımlayınız ve veri setine değişken olarak ekleyiniz.
# Yeni eklenecek değişkenin adı: customers_level_based
# Önceki soruda elde edeceğiniz çıktıdaki gözlemleri bir araya getirerek customers_level_based değişkenini oluşturmanız gerekmektedir.
# Dikkat! List comprehension ile customers_level_based değerleri oluşturulduktan sonra bu değerlerin tekilleştirilmesi gerekmektedir.
# Örneğin birden fazla şu ifadeden olabilir: USA_ANDROID_MALE_0_18. Bunları groupby'a alıp price ortalamalarını almak gerekmektedir.

def birlestirici(x,y,z,t):
    return x.upper() + "_" + y.upper() + "_" + z.upper() + "_" + t.upper()

agg_df["CUSTOMERS_LEVEL_BASED"]=[birlestirici(var1,var2,var3,var4) for (var1,var2,var3,var4) in zip(agg_df["COUNTRY"],agg_df["SOURCE"],agg_df["SEX"],agg_df["AGE_CAT"])]
agg_df

agg_df=agg_df.groupby("CUSTOMERS_LEVEL_BASED").agg({"PRICE":"mean"})
agg_df.reset_index(inplace=True)
agg_df

#Burak's Way
agg_df["AGE_CAT"] = agg_df["AGE_CAT"].astype("object")

agg_df['CUSTOMERS_LEVEL_BASED'] = agg_df["COUNTRY"] + "_" \
                                  + agg_df["SOURCE"] + "_" \
                                  + agg_df["SEX"] + "_"\
                                  + agg_df["AGE_CAT"]

agg_df['CUSTOMERS_LEVEL_BASED'] = agg_df['CUSTOMERS_LEVEL_BASED'].str.upper()
agg_df = agg_df.groupby("CUSTOMERS_LEVEL_BASED").agg({"PRICE": "mean"})
agg_df.reset_index(inplace=True)
agg_df

# Another way
# çalışmadı
agg_df.values
for row in agg_df.values:
    print(row)

df["CUSTOMERS_LEVEL_BASED"]=[ row[0].upper() + "_" + row[1].upper() + "_" + row[2].upper() + "_" + row[5].upper() for row in agg_df.values]

# Görev 7: Yeni müşterileri (personaları) segmentlere ayırınız.
# Yeni müşterileri (Örnek: USA_ANDROID_MALE_0_18) PRICE’a göre 4 segmente ayırınız.
# Segmentleri SEGMENT isimlendirmesi ile değişken olarak agg_df’e ekleyiniz.
# Segmentleri betimleyiniz (Segmentlere göre group by yapıp price mean, max, sum’larını alınız).


agg_df["SEGMENT"]=pd.qcut(agg_df["PRICE"], 4, labels=["D","C","B","A"])
agg_df

agg_df.groupby("SEGMENT").agg({"PRICE":["mean", "max", "sum"]})


# Görev 8: Yeni gelen müşterileri sınıflandırıp, ne kadar gelir getirebileceklerini tahmin ediniz.
# 33 yaşında ANDROID kullanan bir Türk kadını hangi segmente aittir ve ortalama ne kadar gelir kazandırması beklenir?
# 35 yaşında IOS kullanan bir Fransız kadını hangi segmente aittir ve ortalama ne kadar gelir kazandırması beklenir?

new_user_1="TUR_ANDROID_FEMALE_31_40"
agg_df[agg_df["CUSTOMERS_LEVEL_BASED"] == new_user_1]

new_user_2="FRA_IOS_FEMALE_31_40"
agg_df[agg_df["CUSTOMERS_LEVEL_BASED"] == new_user_2]
