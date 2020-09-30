export function intersection(setA, setB) {
    const _intersection = new Set()
    for (const elem of setB) {
        if (setA.has(elem)) {
            _intersection.add(elem)
        }
    }
    return _intersection
}

export function isSuperset(set, subset) {
    for (let elem of subset) {
        if (!set.has(elem)) {
            return false
        }
    }
    return true
}

export function equal(setA, setB) {
    if (setA.size !== setB.size) {
        return false
    }

    return isSuperset(setA, setB) && isSuperset(setB, setA)
}
