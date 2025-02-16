import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import time

# Apply Seaborn Style
sns.set_style("whitegrid")

# Function to update and display sorting visualization
def update_bars(arr, colors, algo_name):
    fig, ax = plt.subplots(figsize=(7, 4))  # High-res visualization
    bars = ax.bar(range(len(arr)), arr, color=colors, edgecolor="black")
    
    # Display values on bars
    for bar, val in zip(bars, arr):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 2, str(val), ha='center', fontsize=10, fontweight='bold', color='black')

    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_title(f"{algo_name} Visualization", fontsize=14, fontweight='bold', color='black')
    ax.set_facecolor('#f5f5f5')
    plt.grid(axis='y', linestyle='--', alpha=0.5)
    st.pyplot(fig)
    time.sleep(0.3)

# Sorting algorithms

def bubble_sort(arr):
    for i in range(len(arr)):
        for j in range(len(arr) - i - 1):
            colors = ['blue'] * len(arr)
            colors[j], colors[j+1] = 'red', 'red'
            update_bars(arr, colors, "Bubble Sort")
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
    update_bars(arr, ['blue'] * len(arr), "Bubble Sort")

def selection_sort(arr):
    for i in range(len(arr)):
        min_idx = i
        for j in range(i+1, len(arr)):
            if arr[j] < arr[min_idx]:
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
        update_bars(arr, ['blue'] * len(arr), "Selection Sort")

def insertion_sort(arr):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and key < arr[j]:
            arr[j + 1] = arr[j]
            j -= 1
            update_bars(arr, ['blue'] * len(arr), "Insertion Sort")
        arr[j + 1] = key
    update_bars(arr, ['blue'] * len(arr), "Insertion Sort")

def merge_sort(arr, left, right):
    if left < right:
        mid = (left + right) // 2
        merge_sort(arr, left, mid)
        merge_sort(arr, mid + 1, right)
        merge(arr, left, mid, right)

def merge(arr, left, mid, right):
    left_part = arr[left:mid+1]
    right_part = arr[mid+1:right+1]
    i = j = 0
    k = left
    while i < len(left_part) and j < len(right_part):
        if left_part[i] < right_part[j]:
            arr[k] = left_part[i]
            i += 1
        else:
            arr[k] = right_part[j]
            j += 1
        k += 1
    while i < len(left_part):
        arr[k] = left_part[i]
        i += 1
        k += 1
    while j < len(right_part):
        arr[k] = right_part[j]
        j += 1
        k += 1
    update_bars(arr, ['blue'] * len(arr), "Merge Sort")

def quick_sort(arr, low=0, high=None):
    if high is None:
        high = len(arr) - 1
    if low < high:
        pi = partition(arr, low, high)
        quick_sort(arr, low, pi - 1)
        quick_sort(arr, pi + 1, high)

def partition(arr, low, high):
    pivot = arr[high]
    i = low - 1
    for j in range(low, high):
        if arr[j] < pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
            update_bars(arr, ['red' if x == i or x == j else 'blue' for x in range(len(arr))], "Quick Sort")
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    update_bars(arr, ['green' if x == i+1 else 'blue' for x in range(len(arr))], "Quick Sort")
    return i + 1

def heap_sort(arr):
    def heapify(arr, n, i):
        largest = i
        left = 2 * i + 1
        right = 2 * i + 2
        if left < n and arr[left] > arr[largest]:
            largest = left
        if right < n and arr[right] > arr[largest]:
            largest = right
        if largest != i:
            arr[i], arr[largest] = arr[largest], arr[i]
            update_bars(arr, ['red' if x == i or x == largest else 'blue' for x in range(len(arr))], "Heap Sort")
            heapify(arr, n, largest)
    n = len(arr)
    for i in range(n // 2 - 1, -1, -1):
        heapify(arr, n, i)
    for i in range(n - 1, 0, -1):
        arr[i], arr[0] = arr[0], arr[i]
        update_bars(arr, ['green' if x == i else 'blue' for x in range(len(arr))], "Heap Sort")
        heapify(arr, i, 0)

# Streamlit UI
st.set_page_config(page_title="Algorithm Visualizer", layout="wide")
st.title("🎨 Algorithm Visualizer - High-End Edition")

# User input
algo_choice = st.selectbox("Select Sorting Algorithm", ["Bubble Sort", "Selection Sort", "Insertion Sort", "Merge Sort", "Quick Sort", "Heap Sort"])
array_size = st.slider("Select Array Size", min_value=5, max_value=30, value=10)
arr = np.random.randint(1, 100, array_size)

col1, col2 = st.columns(2)
col1.write("**Unsorted Array:**")
col1.write(arr)

if st.button("Start Sorting"):
    sorted_arr = arr.copy()
    eval(f"{algo_choice.lower().replace(' ', '_')}(sorted_arr)")
    col2.write("**Sorted Array:**")
    col2.write(sorted_arr)
