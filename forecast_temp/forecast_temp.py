import numpy as np
from sklearn.linear_model import LinearRegression


# def forecast_temperature(temps):
#     """
#     temps is a list of temperature, has 192 values
#     """
#     # Every record is 30 minutes, seperate
#     per_hour_temps = np.array(temps)

#     # Average temperature of each days
#     avg_each_days = [0] * 4
#     for i in range(4):
#         avg_each_days[i] = np.average(per_hour_temps[i*48:i*48+48])

#     # Seasonal index of each 30 minutes within a day
#     seasonal_idx = [0] * per_hour_temps.shape[0]
#     for i in range(4):
#         seasonal_idx[i*48:i*48+48] = \
#             per_hour_temps[i*48:i*48+48] / avg_each_days[i]

#     # Predict the new index of the forecast day
#     predict_idx = [0] * 48
#     for i in range(48):
#         predict_idx[i] = 0.25 * (seasonal_idx[i] + seasonal_idx[48+i] +
#                                  seasonal_idx[96+i] + seasonal_idx[144+i])

#     # Linearly guessing the new average value
#     def linear_guess(arr):
#         reg = LinearRegression().fit(np.arange(len(arr)).reshape(-1, 1),
#                                      np.array(arr).reshape(-1, 1))
#         return reg.predict([[len(arr)]])[0][0].item()

#     # Calculate new average value
#     avg = np.average(avg_each_days)
#     linear_val = linear_guess(avg_each_days)
#     predict_temp = 0.5 * (avg + linear_val)

#     # Multiply the index the guess the final 30 minutes gap temperature
#     predict_temp_30_min = np.array(predict_idx) * predict_temp

#     # Reduce from 30 minutes gap to 1 hour gap
#     even_idx_temps = predict_temp_30_min[::2]
#     odd_idx_temps = predict_temp_30_min[1::2]
#     predict_temp_hour = 0.5 * (even_idx_temps + odd_idx_temps)

#     return np.rint(predict_temp_hour).astype(int).tolist()

def forecast_temperature(temps):
    """
    temps is a list of temperatures, has at least 192 values
    """
    # Separate data into pre-00:00 and post-00:00
    pre_midnight_temps = np.array(temps[:192])
    post_midnight_temps = np.array(temps[192:])

    # Average temperature of each day (pre-00:00 and post-00:00)
    avg_each_days = [0] * 4
    for i in range(4):
        avg_each_days[i] = np.average(pre_midnight_temps[i*48:i*48+48])

    # Seasonal index of each 30 minutes within a day (pre-00:00 and post-00:00)
    seasonal_idx_pre_midnight = [0] * pre_midnight_temps.shape[0]

    for i in range(4):
        seasonal_idx_pre_midnight[i*48:i*48+48] = pre_midnight_temps[i*48:i*48+48] / avg_each_days[i]

    # Predict the new index of the forecast day (pre-00:00 and post-00:00)
    predict_idx_pre_midnight = [0] * 48

    for i in range(48):
        predict_idx_pre_midnight[i] = 0.25 * (seasonal_idx_pre_midnight[i] + seasonal_idx_pre_midnight[48+i] +
                                              seasonal_idx_pre_midnight[96+i] + seasonal_idx_pre_midnight[144+i])

    # Linearly guessing the new average value (pre-00:00)
    def linear_guess(arr):
        reg = LinearRegression().fit(np.arange(len(arr)).reshape(-1, 1), np.array(arr).reshape(-1, 1))
        return reg.predict([[len(arr)]])[0][0].item()

    # Calculate new average value (pre-00:00)
    avg_pre_midnight = np.average(avg_each_days)
    linear_val_pre_midnight = linear_guess(avg_each_days)
    predict_temp_pre_midnight = 0.5 * (avg_pre_midnight + linear_val_pre_midnight)

    # Multiply the index to guess the final 30 minutes gap temperature (pre-00:00)
    predict_temp_30_min_pre_midnight = np.array(predict_idx_pre_midnight) * predict_temp_pre_midnight

    # Reduce from 30 minutes gap to 1-hour gap (pre-00:00)
    even_idx_temps_pre_midnight = predict_temp_30_min_pre_midnight[::2]
    odd_idx_temps_pre_midnight = predict_temp_30_min_pre_midnight[1::2]
    predict_temp_hour_pre_midnight = 0.5 * (even_idx_temps_pre_midnight + odd_idx_temps_pre_midnight)

    # Combine the predicted temperatures of pre-00:00
    predict_temp_hour = np.concatenate((predict_temp_hour_pre_midnight, post_midnight_temps[:48]))

    return np.rint(predict_temp_hour).astype(int).tolist()