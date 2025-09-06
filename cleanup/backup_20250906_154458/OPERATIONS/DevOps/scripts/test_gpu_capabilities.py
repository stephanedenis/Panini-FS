
# Quick GPU capability test for PaniniFS
import numpy as np
import time

def test_gpu_availability():
    """Test basic GPU availability and performance"""
    try:
        import cupy as cp
        print("✅ CuPy available")
        
        # Test basic GPU operations
        size = 1000
        cpu_array = np.random.random((size, size))
        
        # CPU baseline
        start_time = time.time()
        cpu_result = np.dot(cpu_array, cpu_array.T)
        cpu_time = time.time() - start_time
        
        # GPU test
        gpu_array = cp.asarray(cpu_array)
        start_time = time.time()
        gpu_result = cp.dot(gpu_array, gpu_array.T)
        cp.cuda.Stream.null.synchronize()  # Wait for completion
        gpu_time = time.time() - start_time
        
        speedup = cpu_time / gpu_time
        print(f"Matrix multiplication {size}x{size}:")
        print(f"  CPU time: {cpu_time:.3f}s")
        print(f"  GPU time: {gpu_time:.3f}s") 
        print(f"  Speedup: {speedup:.2f}x")
        
        # Memory test
        memory_info = cp.cuda.Device().mem_info
        free_memory = memory_info[0] / 1024**3
        total_memory = memory_info[1] / 1024**3
        print(f"GPU Memory: {free_memory:.1f}GB free / {total_memory:.1f}GB total")
        
        return {
            "gpu_available": True,
            "speedup": speedup,
            "free_memory_gb": free_memory,
            "total_memory_gb": total_memory
        }
        
    except ImportError:
        print("❌ CuPy not available - install with: pip install cupy")
        return {"gpu_available": False, "error": "CuPy not installed"}
    except Exception as e:
        print(f"❌ GPU test failed: {e}")
        return {"gpu_available": False, "error": str(e)}

if __name__ == "__main__":
    result = test_gpu_availability()
    print("\nTest result:", result)
