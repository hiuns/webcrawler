import concurrent.futures
import time
import hashlib
import random


# Simulate URL processing
def process_url(url):
    try:
        # Simulate random processing time and occasional failures
        time.sleep(random.uniform(0.5, 1.5))
        if random.random() < 0.2:  # 20% chance of failure
            raise Exception(f"Failed to process {url}")
        # Simulate processing by returning a hash of the URL
        return hashlib.sha256(url.encode()).hexdigest()
    except Exception as e:
        return f"Error: {str(e)}"


# Batch processor using threads/processes
def process_batches(urls, batch_size, use_threads=True):
    def process_batch(batch):
        results = []
        with (
            concurrent.futures.ThreadPoolExecutor()
            if use_threads
            else concurrent.futures.ProcessPoolExecutor()
        ) as executor:
            future_to_url = {
                executor.submit(process_url, url): url for url in batch
            }
            for future in concurrent.futures.as_completed(future_to_url):
                url = future_to_url[future]
                try:
                    results.append((url, future.result()))
                except Exception as e:
                    results.append((url, f"Error: {str(e)}"))
        return results

    # Split URLs into batches
    batches = [
        urls[i : i + batch_size] for i in range(0, len(urls), batch_size)
    ]

    # Process each batch
    all_results = []
    for batch in batches:
        print(f"Processing batch: {batch}")
        batch_results = process_batch(batch)
        all_results.extend(batch_results)

    return all_results


if __name__ == "__main__":
    # Simulated list of URLs
    url_list = [f"http://example.com/page{i}" for i in range(1, 51)]
    batch_size = 5

    # Process using threads
    print("Processing with threads...")
    results = process_batches(url_list, batch_size, use_threads=True)
    for url, result in results:
        print(f"{url} -> {result}")

    # Process using processes (comment if not CPU-bound)
    print("\nProcessing with processes...")
    results = process_batches(url_list, batch_size, use_threads=False)
    for url, result in results:
        print(f"{url} -> {result}")
