import pandas as pd
import numpy as np
import math

def scoreValue(df):
    df2 = df[['speed','time']].copy()
    df2 = df2[0:-1]
    df21 = df2[0:1]
    df3 = df21.append(df2)
    df3.reset_index(inplace=True)
    df3.drop(columns = ['index'],inplace = True)

    df['start_time'] = pd.to_datetime(df['time'])
    df['end_time'] = pd.to_datetime(df3['time'])

    df['time_diff'] = ( df.start_time-df.end_time)
    df['del_speed'] = ( df3['speed']-df['speed'])
    df['time_diff'] = df['time_diff'].dt.total_seconds()
    df['acc m/s2'] = ((df['del_speed']/.0002777 )*7.7160494*0.00001)

    A = (df['Latitude'][:-2],df['Longitude'][:-2])
    B = (df['Latitude'][1:-1],df['Longitude'][1:-1])
    C = (df['Latitude'][2:],df['Longitude'][2:])
    a = np.radians(np.array(A))
    b = np.radians(np.array(B))
    c = np.radians(np.array(C))
    avec = a - b
    cvec = c - b
    lat = b[:][0]
    avec[1] *= np.cos(lat)
    cvec[1] *= np.cos(lat)

    u = avec
    v = cvec
    i = u.T
    j = v.T
    df['angle'] = 0

    k= 0;
    for u,v in zip(i,j):
        if (np.dot(u, v) / (np.linalg.norm(u) * np.linalg.norm(v)))<-1.0:
            df['angle'][k] =  np.degrees(math.acos(math.ceil(np.dot(u, v) / (np.linalg.norm(u) * np.linalg.norm(v)))))
        elif np.dot(u, v) / (np.linalg.norm(u) * np.linalg.norm(v)) > 1.000000000000000:
            df['angle'][k] =  np.degrees(math.acos(np.dot(u, v) / (np.linalg.norm(u) * np.linalg.norm(v))-(np.dot(u, v) / (np.linalg.norm(u) * np.linalg.norm(v))-1)))
        else:
            df['angle'][k] =  np.degrees(math.acos(np.dot(u, v) / (np.linalg.norm(u) * np.linalg.norm(v))))
        k=k+1

    df['angle'] = 180.0 - df['angle']
    df2 = df['angle'][:]
    df2 = df2.shift(2)
    df2[0] = 0
    df2[1] = 0
    df['angle']=  df2[:]
    df['angular speed'] = 0.0
    df['angular speed'] =  df['angle']*df['speed']

    df.time_diff[df.time_diff != 1.0] = 0

    df['angular speed'] = df['angular speed']*df['time_diff'] 
    df['acc m/s2'] = df['acc m/s2']*df['time_diff'] 

    df['EventName'] = np.where(df['acc m/s2']>2.745, 'Harsh Acceleration', np.where(df['acc m/s2']<-2.745, 'Harsh Braking',np.where(df['angular speed']>1000, 'Harsh Turn','Normal')))

    item_counts = df["EventName"].value_counts()
    item_counts = pd.DataFrame(item_counts)
    item_counts.reset_index(inplace=True)
    array = {'Harsh Acceleration': 0,
    'Harsh Braking': 0,
    'Harsh Turn': 0,
    'Normal': 0}
    last = np.array(item_counts)
    for i in last:
        array[i[0]]=i[1]
    return(array)