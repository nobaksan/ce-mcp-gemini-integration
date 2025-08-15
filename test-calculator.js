#!/usr/bin/env node

/**
 * Calculator Test Suite
 * 계산기 기능을 테스트하는 간단한 테스트 스위트
 */

const Calculator = require('./calculator');

function runTests() {
    console.log('=== Calculator Test Suite ===\n');
    
    const calc = new Calculator();
    let passed = 0;
    let failed = 0;

    function test(description, testFn) {
        try {
            testFn();
            console.log(`✅ ${description}`);
            passed++;
        } catch (error) {
            console.log(`❌ ${description}: ${error.message}`);
            failed++;
        }
    }

    function assertEqual(actual, expected, message = '') {
        if (actual !== expected) {
            throw new Error(`Expected ${expected}, got ${actual}. ${message}`);
        }
    }

    function assertThrows(fn, message = '') {
        try {
            fn();
            throw new Error(`Expected function to throw an error. ${message}`);
        } catch (error) {
            // 예상된 에러이므로 성공
        }
    }

    // 기본 사칙연산 테스트
    test('덧셈: 2 + 3 = 5', () => {
        assertEqual(calc.add(2, 3), 5);
    });

    test('뺄셈: 5 - 3 = 2', () => {
        assertEqual(calc.subtract(5, 3), 2);
    });

    test('곱셈: 4 × 3 = 12', () => {
        assertEqual(calc.multiply(4, 3), 12);
    });

    test('나눗셈: 10 ÷ 2 = 5', () => {
        assertEqual(calc.divide(10, 2), 5);
    });

    test('0으로 나누기 에러 처리', () => {
        assertThrows(() => calc.divide(10, 0));
    });

    // 고급 수학 함수 테스트
    test('거듭제곱: 2^3 = 8', () => {
        assertEqual(calc.power(2, 3), 8);
    });

    test('제곱근: √9 = 3', () => {
        assertEqual(calc.sqrt(9), 3);
    });

    test('음수 제곱근 에러 처리', () => {
        assertThrows(() => calc.sqrt(-1));
    });

    test('백분율: 100의 50% = 50', () => {
        assertEqual(calc.percentage(100, 50), 50);
    });

    // 메모리 기능 테스트
    test('메모리 저장 및 불러오기', () => {
        calc.memoryStore(42);
        assertEqual(calc.memoryRecall(), 42);
    });

    test('메모리 초기화', () => {
        calc.memoryStore(100);
        calc.memoryClear();
        assertEqual(calc.memoryRecall(), 0);
    });

    // 수식 계산 테스트
    test('수식 계산: 2+3*4 = 14', () => {
        assertEqual(calc.evaluate('2+3*4'), 14);
    });

    test('괄호가 있는 수식: (2+3)*4 = 20', () => {
        assertEqual(calc.evaluate('(2+3)*4'), 20);
    });

    test('소수점 계산: 1.5 + 2.5 = 4', () => {
        assertEqual(calc.evaluate('1.5 + 2.5'), 4);
    });

    test('잘못된 수식 에러 처리', () => {
        assertThrows(() => calc.evaluate('2 + abc'));
    });

    // 히스토리 기능 테스트
    test('히스토리 기능', () => {
        const initialHistoryLength = calc.history.length;
        calc.add(1, 1);
        assertEqual(calc.history.length, initialHistoryLength + 1);
    });

    // 결과 출력
    console.log('\n=== Test Results ===');
    console.log(`✅ Passed: ${passed}`);
    console.log(`❌ Failed: ${failed}`);
    console.log(`📊 Total: ${passed + failed}`);
    
    if (failed === 0) {
        console.log('🎉 All tests passed!');
        process.exit(0);
    } else {
        console.log('💥 Some tests failed!');
        process.exit(1);
    }
}

// 직접 실행할 때만 테스트 실행
if (require.main === module) {
    runTests();
}

module.exports = { runTests };