//
//  InputField.swift
//  app
//
//  Created by Lucas Grant on 2025-07-25.
//
import SwiftUI

struct InputField: View {
    @Binding var inputText: String
    
    @State var focusState: FocusState<Bool>.Binding
    @State var inputLength: Int = 0
    
    let placeholderText: String
    
    init(
        _ inputText: Binding<String>,
        _ focusState: FocusState<Bool>.Binding,
        placeholderText: String
    ) {
        self._inputText = inputText
        self.focusState = focusState
        self.placeholderText = placeholderText
    }
    
    var body: some View {
        VStack {
            ZStack(alignment: .topLeading){
                TextField(
                    "",
                    text: $inputText,
                    axis: .vertical
                )
                .lineLimit(2...5)
                .basicText(size: 14)
                .focused(focusState)
                
                if inputText.isEmpty {
                    Text(placeholderText)
                        .placeholderText(size: 14)
                        .allowsHitTesting(false)
                }
            }
            
            HStack {
                Spacer()
                Text("\(inputLength.description) / \(Const.promptLimit.description)")
                    .allowsHitTesting(false)
                    .foregroundColor(inputLength <= 500 ? CustomColor.white : Color.red)
                    .basicText(size: 14)
            }
        }
        .roundedBox()
        .onChange(of: inputText) {
            inputLength = inputText.count
        }
//        .nAppear() {
////            focusState.wrappedValue = true
//        }
    }
}

#Preview {
    ContentView(.conversation)
}
