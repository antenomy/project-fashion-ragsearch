//
//  CircleButton.swift
//  app
//
//  Created by Lucas Grant on 2025-07-26.
//

import SwiftUI

struct CapsuleButton: View {
    let iconPath: String?
    let text: String?
    let outlineBool: Bool
    let backgroundBool: Bool
    let wideShape: Bool
    
    init(
        text : String? = nil,
        icon iconPath : String? = nil,
        outline: Bool = true,
        background: Bool = true,
        wideShape: Bool = true
    ) {
        self.iconPath = iconPath
        self.text = text
        self.outlineBool = outline
        self.backgroundBool = background
        self.wideShape = wideShape
    }
    
    var body: some View {
        HStack {
            if let text {
                Text(text)
                    .basicText(size: 16)
            }
            
            if let iconPath {
                Image(systemName: iconPath)
                    .font(.system(size: 16))
                    .fontWeight(.bold)
                    .foregroundColor(CustomColor.white)
            }
        }
        .padding(.horizontal, 16)
        .frame(height: 40)
        .frame(maxWidth: wideShape ? .infinity : nil)
        .if(backgroundBool) {view in
            view
                .background(CustomColor.gray)
        }
        .clipShape(Capsule())
        .if(outlineBool) { view in
            view
                .overlay(
                    Capsule()
                        .stroke(CustomColor.lightGray, lineWidth: 2)
                )
        }
    }
}

#Preview {
    ContentView(.conversation)
}
