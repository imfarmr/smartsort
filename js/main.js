document.addEventListener('DOMContentLoaded', function() {
    initNavigation();
    initDocTabs();
    initDemo();
    initScrollEffects();
});

function initNavigation() {
    const navLinks = document.querySelectorAll('.nav-link');
    const sections = document.querySelectorAll('section');
    
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const targetId = this.getAttribute('href').substring(1);
            const targetSection = document.getElementById(targetId);
            
            if (targetSection) {
                const offsetTop = targetSection.offsetTop - 80;
                window.scrollTo({
                    top: offsetTop,
                    behavior: 'smooth'
                });
            }
            
            navLinks.forEach(l => l.classList.remove('active'));
            this.classList.add('active');
        });
    });
    
    window.addEventListener('scroll', () => {
        let current = '';
        sections.forEach(section => {
            const sectionTop = section.offsetTop - 100;
            const sectionHeight = section.clientHeight;
            if (window.pageYOffset >= sectionTop && window.pageYOffset < sectionTop + sectionHeight) {
                current = section.getAttribute('id');
            }
        });
        
        navLinks.forEach(link => {
            link.classList.remove('active');
            if (link.getAttribute('href') === `#${current}`) {
                link.classList.add('active');
            }
        });
    });
}

function initDocTabs() {
    const tabs = document.querySelectorAll('.doc-tab');
    const panels = document.querySelectorAll('.doc-panel');
    
    tabs.forEach(tab => {
        tab.addEventListener('click', function() {
            const targetPanel = this.getAttribute('data-tab');
            
            tabs.forEach(t => t.classList.remove('active'));
            panels.forEach(p => p.classList.remove('active'));
            
            this.classList.add('active');
            document.getElementById(targetPanel).classList.add('active');
        });
    });
}

function initDemo() {
    const generateBtn = document.getElementById('generateBtn');
    const dataTypeSelect = document.getElementById('dataType');
    const arraySizeInput = document.getElementById('arraySize');
    const sizeValue = document.getElementById('sizeValue');
    
    arraySizeInput.addEventListener('input', function() {
        sizeValue.textContent = this.value;
    });
    
    generateBtn.addEventListener('click', function() {
        const dataType = dataTypeSelect.value;
        const size = parseInt(arraySizeInput.value);
        
        const data = generateData(dataType, size);
        displayArray(data, 'inputArray');
        
        const analysis = analyzeData(data);
        displayAnalysis(analysis);
        
        const result = smartSort(data);
        displayArray(result.sorted, 'sortedArray');
        displayStatistics(result.stats);
    });
    
    generateBtn.click();
}

function generateData(type, size) {
    let data = [];
    
    switch(type) {
        case 'random':
            for (let i = 0; i < size; i++) {
                data.push(Math.floor(Math.random() * 100) + 1);
            }
            break;
            
        case 'sorted':
            for (let i = 1; i <= size; i++) {
                data.push(i);
            }
            break;
            
        case 'reverse':
            for (let i = size; i > 0; i--) {
                data.push(i);
            }
            break;
            
        case 'nearlySorted':
            for (let i = 1; i <= size; i++) {
                data.push(i);
            }
            const swaps = Math.max(1, Math.floor(size / 10));
            for (let i = 0; i < swaps; i++) {
                const idx1 = Math.floor(Math.random() * size);
                const idx2 = Math.floor(Math.random() * size);
                [data[idx1], data[idx2]] = [data[idx2], data[idx1]];
            }
            break;
            
        case 'denseRange':
            for (let i = 0; i < size; i++) {
                data.push(Math.floor(Math.random() * 10));
            }
            break;
    }
    
    return data;
}

function analyzeData(data) {
    const presortedness = calculatePresortedness(data);
    const rangeDensity = calculateRangeDensity(data);
    const hasDuplicates = new Set(data).size !== data.length;
    const range = [Math.min(...data), Math.max(...data)];
    
    return {
        size: data.length,
        presortedness: presortedness,
        rangeDensity: rangeDensity,
        hasDuplicates: hasDuplicates,
        range: range
    };
}

function calculatePresortedness(data) {
    if (data.length <= 1) return 1.0;
    
    let inversions = 0;
    const maxInversions = (data.length * (data.length - 1)) / 2;
    
    for (let i = 0; i < data.length - 1; i++) {
        for (let j = i + 1; j < data.length; j++) {
            if (data[i] > data[j]) {
                inversions++;
            }
        }
    }
    
    return 1 - (inversions / maxInversions);
}

function calculateRangeDensity(data) {
    if (data.length === 0) return 0;
    
    const min = Math.min(...data);
    const max = Math.max(...data);
    const range = max - min;
    
    if (range === 0) return 1.0;
    
    const uniqueCount = new Set(data).size;
    return uniqueCount / (range + 1);
}

function selectStrategy(analysis) {
    if (analysis.size <= 20) {
        return 'InsertionSort';
    }
    
    if (analysis.presortedness >= 0.7) {
        return 'InsertionSort';
    }
    
    const valueRange = analysis.range[1] - analysis.range[0];
    if (analysis.rangeDensity >= 0.01 && valueRange < analysis.size * 10 && analysis.range[0] >= 0) {
        return 'RadixSort';
    }
    
    return 'MergeSort';
}

function smartSort(data) {
    const startTime = performance.now();
    let comparisons = 0;
    let swaps = 0;
    
    const analysis = analyzeData(data);
    const strategy = selectStrategy(analysis);
    
    let sorted;
    if (strategy === 'InsertionSort') {
        const result = insertionSort([...data]);
        sorted = result.array;
        comparisons = result.comparisons;
        swaps = result.swaps;
    } else if (strategy === 'RadixSort') {
        const result = radixSort([...data]);
        sorted = result.array;
        comparisons = result.comparisons;
        swaps = result.swaps;
    } else {
        const result = mergeSort([...data]);
        sorted = result.array;
        comparisons = result.comparisons;
        swaps = result.swaps;
    }
    
    const endTime = performance.now();
    
    return {
        sorted: sorted,
        stats: {
            strategy: strategy,
            comparisons: comparisons,
            swaps: swaps,
            time: (endTime - startTime).toFixed(4),
            presortedness: (analysis.presortedness * 100).toFixed(1),
            rangeDensity: (analysis.rangeDensity * 100).toFixed(1)
        }
    };
}

function insertionSort(arr) {
    let comparisons = 0;
    let swaps = 0;
    
    for (let i = 1; i < arr.length; i++) {
        let key = arr[i];
        let j = i - 1;
        
        while (j >= 0 && arr[j] > key) {
            comparisons++;
            arr[j + 1] = arr[j];
            swaps++;
            j--;
        }
        if (j >= 0) comparisons++;
        arr[j + 1] = key;
    }
    
    return { array: arr, comparisons, swaps };
}

function mergeSort(arr) {
    let comparisons = 0;
    let swaps = 0;
    
    function merge(left, right) {
        let result = [];
        let i = 0, j = 0;
        
        while (i < left.length && j < right.length) {
            comparisons++;
            if (left[i] <= right[j]) {
                result.push(left[i]);
                i++;
            } else {
                result.push(right[j]);
                j++;
            }
            swaps++;
        }
        
        while (i < left.length) {
            result.push(left[i]);
            i++;
            swaps++;
        }
        
        while (j < right.length) {
            result.push(right[j]);
            j++;
            swaps++;
        }
        
        return result;
    }
    
    function sort(array) {
        if (array.length <= 1) return array;
        
        const mid = Math.floor(array.length / 2);
        const left = sort(array.slice(0, mid));
        const right = sort(array.slice(mid));
        
        return merge(left, right);
    }
    
    const sorted = sort(arr);
    return { array: sorted, comparisons, swaps };
}

function radixSort(arr) {
    let comparisons = 0;
    let swaps = 0;
    
    const max = Math.max(...arr);
    let exp = 1;
    
    while (Math.floor(max / exp) > 0) {
        const buckets = Array.from({ length: 10 }, () => []);
        
        for (let i = 0; i < arr.length; i++) {
            const digit = Math.floor(arr[i] / exp) % 10;
            buckets[digit].push(arr[i]);
            comparisons++;
        }
        
        arr = [];
        for (let bucket of buckets) {
            arr.push(...bucket);
            swaps += bucket.length;
        }
        
        exp *= 10;
    }
    
    return { array: arr, comparisons, swaps };
}

function displayArray(data, elementId) {
    const element = document.getElementById(elementId);
    element.textContent = `[${data.join(', ')}]`;
}

function displayAnalysis(analysis) {
    const element = document.getElementById('analysis');
    const strategy = selectStrategy(analysis);
    
    element.innerHTML = `
        <div><strong>Size:</strong> ${analysis.size} elements</div>
        <div><strong>Presortedness:</strong> ${(analysis.presortedness * 100).toFixed(1)}%</div>
        <div><strong>Range Density:</strong> ${(analysis.rangeDensity * 100).toFixed(1)}%</div>
        <div><strong>Has Duplicates:</strong> ${analysis.hasDuplicates ? 'Yes' : 'No'}</div>
        <div><strong>Range:</strong> [${analysis.range[0]}, ${analysis.range[1]}]</div>
        <div style="margin-top: 12px; padding-top: 12px; border-top: 1px solid var(--border-color);">
            <strong>Selected Strategy:</strong> <span style="color: var(--accent-primary);">${strategy}</span>
        </div>
    `;
}

function displayStatistics(stats) {
    const element = document.getElementById('statistics');
    
    element.innerHTML = `
        <div><strong>Strategy Used:</strong> <span style="color: var(--accent-primary);">${stats.strategy}</span></div>
        <div><strong>Execution Time:</strong> ${stats.time} ms</div>
        <div><strong>Comparisons:</strong> ${stats.comparisons.toLocaleString()}</div>
        <div><strong>Swaps:</strong> ${stats.swaps.toLocaleString()}</div>
        <div style="margin-top: 12px; padding-top: 12px; border-top: 1px solid var(--border-color);">
            <div><strong>Presortedness:</strong> ${stats.presortedness}%</div>
            <div><strong>Range Density:</strong> ${stats.rangeDensity}%</div>
        </div>
    `;
}

function initScrollEffects() {
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -100px 0px'
    };
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, observerOptions);
    
    const cards = document.querySelectorAll('.feature-card, .usage-card, .algorithm-card');
    cards.forEach(card => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        card.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        observer.observe(card);
    });
}
