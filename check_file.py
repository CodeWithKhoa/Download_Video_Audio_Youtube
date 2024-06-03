import os
import sys
import psutil
from pydub import AudioSegment
from pydub.exceptions import CouldntDecodeError
from mutagen.mp3 import MP3, HeaderNotFoundError
from concurrent.futures import ThreadPoolExecutor, as_completed

# Tạo một biến cờ để kiểm tra xem một KeyboardInterrupt đã được ném hay không
interrupt_flag = False

def check_mp3_file(file_path):
    global interrupt_flag
    try:
        if interrupt_flag:
            return file_path, False

        # Kiểm tra file MP3 bằng mutagen trước
        mp3_info = MP3(file_path)
        
        # Chỉ đọc một phần của file thay vì toàn bộ file
        audio = AudioSegment.from_file(file_path)
        duration = len(audio)
        if duration > 1000:
            audio[:1000]  # Kiểm tra 1 giây đầu tiên của file
        print(f"File '{file_path}' is a valid mp3 file and can be played.")
        return file_path, True
    except KeyboardInterrupt:
        print("KeyboardInterrupt detected. Cleaning up...")
        interrupt_flag = True  # Đặt cờ khi có ngoại lệ KeyboardInterrupt
        return file_path, False
    except (HeaderNotFoundError, CouldntDecodeError):
        print(f"File '{file_path}' is not a valid mp3 file or is corrupted. Deleting...")
        if not interrupt_flag:
            os.remove(file_path)
        return file_path, False
    except Exception as e:
        print(f"An error occurred with file '{file_path}': {e}. Deleting...")
        if not interrupt_flag:
            os.remove(file_path)
        return file_path, False

def check_mp3_files_in_directory(directory):
    global interrupt_flag
    files_to_check = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".mp3"):
                file_path = os.path.join(root, file)
                files_to_check.append(file_path)

    stt = 0
    sl_delete = 0
    with ThreadPoolExecutor() as executor:
        future_to_file = {executor.submit(check_mp3_file, file_path): file_path for file_path in files_to_check}
        for future in as_completed(future_to_file):
            try:
                file_path, is_valid = future.result()
                stt += 1
                print(f" {stt} - ", end="")
                if not is_valid:
                    sl_delete += 1
            except KeyboardInterrupt:
                print("KeyboardInterrupt detected. Cleaning up...")
                interrupt_flag = True  # Đặt cờ khi có ngoại lệ KeyboardInterrupt
                break  # Dừng vòng lặp khi có ngoại lệ KeyboardInterrupt
            except Exception as e:
                print(f"An error occurred: {e}")

    print(f"Total Files: {stt}")
    print(f"Files Deleted: {sl_delete}")

# Kiểm tra xem file có đang được sử dụng bởi bất kỳ quy trình nào hay không
def is_file_in_use(file_path):
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            for item in proc.open_files():
                if file_path == item.path:
                    return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False

# Thử kiểm tra tất cả file mp3 trong một thư mục
directory_path = input("Enter the path to the Folder: ")
check_mp3_files_in_directory(directory_path)
