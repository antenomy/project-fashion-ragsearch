//
//  ErrorEnums.swift
//  ragSearch
//
//  Created by Lucas Grant on 2025-08-01.
//

enum ItemHandlerError: Error {
    case invalidURL
    case uhoh
}

// Function Errors
enum GetItemError: Error {
    // Sub Function Errors
    case invalidResponse
    case invalidData(Error)
}

enum EditItemError: Error {
    // Sub Function Errors
    case invalidResponse(Int)
    case encodingFailed(Error)
    case invalidData(Error)
}

