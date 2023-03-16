import csv

def count_zeros_in_csv(csv_file_path):
    zero_count = 0
    nonzero_count = 0
    error_count = 0
    total_count = 0
    with open(csv_file_path, 'r') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            for number in row:
                total_count += 1
                try:
                    float_number = float(number)
                    if float_number == 0.0:
                        zero_count += 1
                    else:
                        nonzero_count += 1
                except ValueError:
                    print(f"Error: {number} cannot be converted to a float")
                    error_count += 1
                    continue
    return zero_count, total_count, nonzero_count, error_count


if __name__ == "__main__":
    pose_csv_4K = r'/home/gsquist/keypoints/11-17-21-on-03-08-23_4K.csv' # 4K
    pose_csv_HD = r'/home/gsquist/keypoints/11-17-21-on-03-13-23_HD.csv'  # HD
    zero_count_4K, total_count_4K, nonzero_count_4K, error_count_4K = count_zeros_in_csv(pose_csv_4K)
    zero_count_HD, total_count_HD, nonzero_count_HD, error_count_HD = count_zeros_in_csv(pose_csv_HD)
    print("zero_count_4K: ", zero_count_4K)
    print("zero_count_HD: ", zero_count_HD)
    print("total_count_4K: ", total_count_4K)
    print("total_count_HD: ", total_count_HD)
    print("nonzero_count_4K: ", nonzero_count_4K)
    print("nonzero_count_HD: ", nonzero_count_HD)
    print("error_count_4K: ", error_count_4K)
    print("error_count_HD", error_count_HD)
    # zero_count_4K:  343897
    # zero_count_HD:  409681
